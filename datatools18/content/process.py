import os
import json
import traceback

import conf.common as config

from content.replic_vars import replic_vars
from content.functions import FunctionLoader

from service.models import *
from service.semantic import TextProcessor
from service.users import UserProcessor
from service.context import ContextProcess
from service.talklogger import TalkLogger
from service.search import SearchEngine

from logic.smalltalk import Smalltalk

class processChat:
    def __init__(self, tonque):
        """Constructor"""
        self.tonque = tonque
        self.medium = ''
        self.context = ContextProcess()
        self.users = UserProcessor()
        self.talklogger = TalkLogger()
        self.search = SearchEngine()
        self.textProcessor = TextProcessor()
        self.smalltalk = Smalltalk(medium=self.medium)
        self.functions = FunctionLoader(self.medium).make_functions_dict()


    def process(self, message):
        """
         - принимает запрос пользователя
         - определяет каким контентом ответить, исходя из фразы и контекста 
         - отдает финальный ответ
         
        """

        user_id  = self.users.get_user_id(message, message['user_id'])

        last_context = self.context.last_context(user_id)

        text, text_raw, emoji  = self.textProcessor.get_content(message)

        meaning_nodes  = self.search.handle_request(text, d_type='words', context=last_context['context'])

        if meaning_nodes:
            response = self.process_function(user_id, meaning_nodes[0], text, text_raw)
        else:
            response = self.smalltalk.not_defined(user_id, text, text_raw, context=last_context)
        
        self.talklogger.asyncStoreInput(user_id, 2, text_raw, context=last_context['context'], function=self.get_answer_type(meaning_nodes))

        return response, user_id, message['user_id']



    def define_callback_content(self, text):
        """Название кнопки в чате можеть состоять из двух частей, разделенных знаком _  тогда вторая 
           часть придет в функцию в параметр meaning
        """
        text_split = text.split('_')

        if len(text_split) > 2:
            ix, content =  '_'.join(text_split[:-1]), '_'.join(text_split[-1:])
        else:
            ix, content = text, 'none'

        return ix, content


    def get_answer_type(self,meaning_nodes):
        if meaning_nodes:
            meaning_node = meaning_nodes[0]
            
            if 'function' in meaning_node:
                answer_type = meaning_node['function']
            elif 'text_var' in meaning_node:
                answer_type = meaning_node['text_var']
            else:
                answer_type = 'text'
        else:
            answer_type = 'not_defined'
        return answer_type



    def process_callback(self, message):
        """
            Обработка запроса аналогично функции process, но для inline-кнопок
        """
        response = None

        user_id  = self.users.get_user_id(message, message['user_id'])
        last_context = self.context.last_context(user_id)

        callback_ix, callback_content = self.define_callback_content(message['callback_data'])

        meaning_nodes  = self.search.handle_request(callback_ix, d_type='words', context=last_context['context'])

        if meaning_nodes:

            meaning_node = meaning_nodes[0]
            meaning_node['callback_content'] = callback_content
            response = self.process_function(user_id, meaning_node, callback_ix, message['callback_data'])
        else:
            response = self.smalltalk.not_defined_callback(user_id, message['callback_data'], '')

        self.talklogger.asyncStoreInput(user_id, 2, message['callback_data'], context=last_context['context'], function=self.get_answer_type(meaning_nodes))

        return response, user_id, message['user_id']



    def process_text(self,user_id,meaning,text, text_raw):
        """обработка статичного ответа"""
         
        response = {}
        for i in ['tts', 'text']:
            if i in meaning:
                if meaning[i]:
                    if 'text_var' in meaning[i]:
                        data = json.loads(meaning[i].replace("'",'"'))
                        response[i] = replic_vars[data['text_var']]
                    else:
                        response[i] = meaning[i]

        if meaning['text_var']:
            response['text'] = replic_vars[meaning['text_var']]

        if 'menu' in meaning:
            response['reply_markup'] =[i['text'] for i in meaning['menu']]

        if 'menu_inline' in meaning:
            response['reply_markup_inline'] = json.loads(meaning['menu_inline'].replace("'", '"'))

        if 'set_context' in meaning:
            response['set_context'] = {'name':meaning['set_context']}

        return response


    def process_function(self, user_id, meaning, text, text_raw):
        """обработка ответа, заданного в виде функции"""

        for i in ['context', 'function', 'menu_inline','audio','set_context']:
            if meaning[i] is None:
                del meaning[i]

        if 'function' in meaning:
            try:
                function_name =self.functions[meaning['function']]
            except:
                s_error = "Функиця не существует: {}".format(meaning['function'])
                raise IndexError(s_error)

            response = function_name(user_id, meaning, text, text_raw)

        else:
            response = self.process_text(user_id, meaning, text, text_raw)

        return response


class processTg(processChat):

    def __init__(self, tonque):
        """Constructor"""
        self.tonque = tonque
        self.medium = 'tg'
        self.context = ContextProcess()
        self.users = UserProcessor()
        self.talklogger = TalkLogger()
        self.search = SearchEngine()
        self.textProcessor = TextProcessor()
        self.smalltalk = Smalltalk(medium=self.medium)
        self.functions = FunctionLoader(self.medium).make_functions_dict()


    def response(self, update):
        
        def send_response(user_id, chat_id, response):
            """отправка одного ответа в телеграм"""
            self.tonque.send_message(user_id, chat_id, response)
            self.talklogger.asyncStoreOutput(user_id, 1, response)
            
        
        def send_response_list(user_id, chat_id, response):
            """отправка нескольких подряд ответов в телеграм"""
            if isinstance(response,(list)):
                for response_bubble in response:
                    send_response(user_id, chat_id, response_bubble)
            else:
                send_response(user_id, chat_id, response)

            return True
            
        
        try:
            
            if update['callback_data']:
                response, user_id, chat_id = self.process_callback(update)
            else:
                response, user_id, chat_id =  self.process(update)

            send_response_list(user_id, chat_id, response)


        except Exception as e:

            tb = traceback.format_exc()
            response = {'text':str(e)+ str(tb)}
            
            json_stored = Loghook(fulljson=str(response), chat_id = 101)
            json_stored.save()

        return response
