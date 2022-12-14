import conf.common as config

import telebot
import emoji
import random

from service.menu import menuChat
from service.ga import gaTracker
from service.models import *
from service.context import ContextProcess

class TonqueTg:
    """Класс через который проходят все сообщения"""

    def __init__(self):
        self.bot = telebot.TeleBot(config.tg_token)
        self.tracker = gaTracker()
        self.menuChat = menuChat()
        self.context = ContextProcess()


    def define_chat_id(self,user_id):
        user = User.get(User.id == user_id)
        return user.chat_id


    def random_text(self, data):

        for i in ['tts','text']:
            if i in data:
                if type(data[i]) == list:
                    data[i] = random.choice(data[i])

        return data


    def set_context(self,user_id,data):

        name = data.get('name', '')
        value = data.get('value', '')

        if name:
            self.context.set_context(user_id, name, value)

    def transform_buttons(self, response):
        if 'reply_markup' in response:
            response['reply_markup'] = self.menuChat.genButtons(response['reply_markup'])

        if 'reply_markup_inline' in response:
            response['reply_markup'] = self.menuChat.genInlineButtons(response['reply_markup_inline'])
            del response['reply_markup_inline']
        return response


    def send_message(self, user_id, chat_id, response):
        """Отправка сообщения"""

        # if chat_id not in [1148068301,1287043873, 1088092144]:

        for i in ['audio','tts','end_session','state']:
            if i in response:
                del response[i]


        response['disable_web_page_preview'] = False

        # json_stored = Loghook(fulljson=str(response), chat_id = 2)#update.message.chat.id)
        # json_stored.save()

        response = self.transform_buttons(response)

        if 'set_context' in response:
            self.set_context(user_id, response['set_context'])
            del response['set_context']

        if 'location' in response:
            location = response['location']
            del response['location']

            self.bot.send_message(chat_id, **response)
            self.send_location(chat_id, location)

        if 'text' in response:

            if type(response['text']) == list:
                response['text'] = random.choice(response['text'])

            response['text'] = emoji.emojize(response['text'])
            self.bot.send_message(chat_id, **response)

        # else:
        #     self.bot.send_message(chat_id, **response)

        url = self.tracker.storeOutputTg(chat_id, response)

        return response


    def send_location(self, chat_id, location):
        """Отправка месторасположения"""
        self.bot.send_location(chat_id, location['lat'], location['lng'])
        self.tracker.storeOutputTg(chat_id, {'text':'location'})
        return True


    def send_photo(self, chat_id, img, caption='', reply_markup=''):
        """Отправка фото"""

        self.bot.send_photo(chat_id, img, caption=caption, reply_markup=reply_markup)
        #self.bot.send_message(chat_id, **response)
        self.tracker.storeOutputMessage(chat_id, {'text':'photo'})
        return True


    def edit_message_caption(self, chat_id, message_id, response):
        """Отправка сообщения"""
        self.bot.edit_message_caption(response[0], chat_id=chat_id, message_id=message_id, reply_markup=response[1])
        return True


    def delete_message(self, chat_id, message_id):
        self.bot.delete_message(chat_id,message_id)
        return True


    def edit_message_text(self, chat_id, message_id, response):
        """Отправка сообщения"""
        response = self.transform_buttons(response)
        if 'text' in response:
            self.bot.edit_message_text(
                                        text=response['text'],
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=response['reply_markup']
                                    )
        else:
            self.bot.edit_message_reply_markup(
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=response['reply_markup']
                                    )

        return True


    def send_alert_admin(self, chat_id, message_id, text):
        """Отправка фото"""
        # for a_id in self.ADMIN_IDS:
        # self.send_message(a_id, {'text': alert_text})
        for a_id in config.admin_ids:
            # self.send_message(a_id, {'text': 'Вопрос от пользователя:'})
            self.bot.forward_message(a_id, chat_id, message_id)



        return True
