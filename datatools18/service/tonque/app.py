
import json
import random
from service.context import ContextProcess


class TonqueApp:

    def __init__(self):
        self.version = "1.0"
        self.context = ContextProcess()


    def random_text(self, data):

        for i in ['tts','text']:
            if i in data:
                if type(data[i]) == list:
                    data[i] = random.choice(data[i])

        return data


    def transform_buttons(self, response):
        """[
            {
                "title": "Надпись на кнопке",
                "payload":'x',
                "url": "https://example.com/",
                "hide": false
            }
        ]"""

        buttons = []

        if 'reply_markup_inline' in response:
            for i in response['reply_markup_inline']:

                b = {
                    "title":i['text'],
                    "hide": "false"
                }

                if 'callback_data' in i:
                    b['payload'] = i['callback_data']

                if 'url' in i:
                    b['url'] = i['url']

                buttons.append(b)

            del response['reply_markup_inline']

        return response, buttons


    def transform_tts(self, response):

        tts_text, tts_audio = '',''
        if 'tts' in response :
            tts_text = response['tts'].replace('\n','')
        else:
            tts_text = response['text']

        if 'audio' in response:

            tts_audio = '<speaker audio="{}.opus">'.format(response['audio'])
            del response['audio']

        tts_text =  "{} {}".format(tts_audio, tts_text)

        arf_replace = '<speaker audio="dialogs-upload/a36047f4-f575-45db-9e58-0e452703ee6e/ee276af6-3324-4841-a4f1-ba25ef674fee.opus">'
        tts_text = tts_text.replace('[arf]', arf_replace)

        response['text'] = response['text'].replace('[arf]','')
        response['tts'] = tts_text


        return response


    def transform_card(self, response):

        if 'card' in response:
            card =  {
                  "type": "BigImage",
                  "image_id": response['card']['image'],
                  "title": response['card']['title'],
                  "description": response['text']
            }
            response['card'] = card
        else:
            pass

        return response


    def set_context(self,user_id,data):

        name = data.get('name', '')
        value = data.get('value', '')

        if name:
            self.context.set_context(user_id, name, value)


    def response_handle(self, user_id, session, response, end_session = False):
        """Формирование ответа в нужном формате для Яндекса"""

        if 'end_session' in response:
            end_session = response['end_session']
            del response['end_session']

        if 'set_context' in response:
            self.set_context(user_id, response['set_context'])
            del response['set_context']

        response_ya = {
            "version": self.version,
            "session": session,
            "response": {"end_session": end_session}
        }

        response = self.random_text(response)
        response, buttons = self.transform_buttons(response)
        response =  self.transform_tts(response)
        response =self.transform_card(response)


        content = {
                  **response,
                  'buttons':buttons,
                  "end_session": end_session
                  }

        response_ya['response'] = content

        return response_ya
