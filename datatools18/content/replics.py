import math
import random

import conf.common as config

from content.replic_vars import replic_vars, get_replic_var
from service.utils import join_enumeration, words_form_d


class ReplicsPhrases():
    def __init__(self):
        pass

    def default_buttons(self):

        buttons = [

                {'text':'Кнопка 1', 'callback_data':'c_set'},
                {'text':'Назад', 'callback_data':'c_drop'}

            ]

        return buttons


    def hello(self):

        text = get_replic_var('hello')

        response = {
            "text":text,
            "set_context":{
                "name":"drop"
                },

            "reply_markup_inline": self.default_buttons()
        }

        return response


    def not_defined(self, input_text=''):

        buttons = [
                {'text':'Оставить пожелание', 'callback_data':'c_feedback'},
                {'text':'Назад', 'callback_data':'c_drop'}
            ]


        response = {
                    'text':get_replic_var('not_defined'),
                    'reply_markup_inline':buttons,
                    'state':input_text
                    }

        return response


    def drop(self):

        text = 'Хорошо, выходим в главное меню.'

        response = {
                'text':text,
                'reply_markup_inline':self.default_buttons(),
                'set_context':{'name':'drop'}
                }

        return response


    def feedback_start(self, chat_id):

        r_menu = [
                {'text':'Отмена', 'callback_data':'c_drop'}
            ]

        text = 'Мы ценим обратную связь! Отправь ваш отзыв в ответ на это сообщение.'

        response = {
                'text':text,
                'reply_markup_inline':r_menu,
                'set_context':{'name':'feedback_text'}
                }

        return response


    def feedback_confirm(self):
        text = 'Сообщение успешно отправлено!'

        response = {
                    'text':text,
                    'reply_markup_inline':self.default_buttons(),
                    'set_context':{'name':'drop'}
                }

        return response




class Replics(ReplicsPhrases):
    def __init__(self):
        pass

    def set_class(self, medium):
        class_dict = {
            'alice':ReplicsAlice(),
            'tg':ReplicsTg(),
            'sber':ReplicsSber()
            }
        return class_dict[medium]



class ReplicsTg(Replics):
    def __init__(self):
        pass
