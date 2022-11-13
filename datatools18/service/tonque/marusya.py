# {
#   "response": {
#     "text": "Сейчас очередь в столовой 5 человек.",
#     "tts": "Сейчас очередь в столовой пять человек.",
#     "buttons": [
#       {
#         "title": "Надпись на кнопке",
#         "payload": {},
#         "url": "https://example.com/"
#       }
#     ],
#     "end_session": true
#   },
#   "session": {
#     "session_id": "574d41e0-a41e-4028-a73a-6f5b5bfed299",
#     "message_id": 0,
#     "user_id": "6953b29afe19e372ecdd34d07b3eae3c2f69b9f04e8cb15e157c4a9e056d58ee"
#   },
#   "version": "1.0"
# }

# {
#   "meta": {
#     "client_id": "MailRu-VC/1.0",
#     "locale": "ru_RU",
#     "timezone": "Europe/Moscow",
#     "interfaces": {
#       "screen": {}
#       }
#    },
#   "request": {
#     "command": "какая очередь в столовой",
#     "original_utterance": "какая очередь в столовой",
#     "type": "SimpleUtterance",
#     "payload": {},
#     "nlu": {
#       "tokens": [
#         "какая",
#         "очередь",
#         "в",
#         "столовой"
#       ]
#     }
#   },
#   "session": {
#     "session_id": "574d41e0-a41e-4028-a73a-6f5b5bfed299",
#     "user_id": "6953b29afe19e372ecdd34d07b3eae3c2f69b9f04e8cb15e157c4a9e056d58ee",
#     "skill_id": "6861e5a9-4e0f-4660-9331-01f720ddaf5d",
#     "new": true,
#     "message_id": 0
#   },
#   "version": "1.0"
# }

# import conf.common as config
# import emoji
import json
# from routing.ga import gaTracker
# from models import *

class TonqueMarusya:

    def __init__(self):
        self.version = "1.0"
        # self.tracker = gaTracker()
        # self.ADMIN_IDS = config.admin_ids


    def transform_buttons(self, response):
        """[
            {
                "title": "Надпись на кнопке",
                "payload":'x',
                "url": "https://example.com/",
                "hide": true
            }
        ]"""

        buttons = []



        if 'reply_markup_inline' in response:
            for i in response['reply_markup_inline']:

                b = {
                    "title":i['text']
                }

                if 'callback_data' in i:
                    b['payload'] = {"callback_data":i['callback_data']}

                if 'url' in i:
                    b['url'] = i['url']

                buttons.append(b)

            del response['reply_markup_inline']

        return buttons

    def transform_tts(self, response):
        # tts = False
        # if 'audio' in response:
        if 'tts' in response:
            tts_text = response['tts']
        else:
            tts_text = response['text']

        return tts_text



    def response_handle(self, session, response, end_session = False):
        """Формирование ответа в нужном формате для Маруси"""

        del session['skill_id']
        del session['new']

        if 'end_session' in response:
            end_session = response['end_session']
            del response['end_session']

        response_fin = {
            "version": self.version,
            "session": session,
        }

        buttons = self.transform_buttons(response)
        tts =  self.transform_tts(response)
        content = {'text':response['text'], 'buttons':buttons, "end_session": end_session}
        if tts:
            content['tts'] = tts
        response_fin['response'] = content


        return json.dumps(response_fin,  ensure_ascii=False,    indent=2)
