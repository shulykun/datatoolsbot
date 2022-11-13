import json
import random
from service.context import ContextProcess


class TonqueSber:

    def __init__(self):
        self.context = ContextProcess()


    def template(self):
        return {'sessionId': '',
         'messageId': 0,
         'uuid': {},

         'messageName': 'ANSWER_TO_USER',

         'payload': {
             'pronounceText': '',
             'pronounceTextType': 'application/text',
             'items': [
                      {'bubble': {}}
                   ],
          'suggestions': {
                    'buttons': [
                              {
                                  'title': 'string',
                                  'action': {}
                              }
                          ]
                     }
           },
          'auto_listening': False,
          'finished': True
        }

    def random_text(self, data):

        for i in ['tts','text']:
            if i in data:
                if type(data[i]) == list:
                    data[i] = random.choice(data[i])

        return data


    def transform_buttons(self, content):
        """
        {'buttons': [
              {
                  'title': 'string',
                  'action': {
                            "type": "text",
                            "text": ""
                        }
              }
          ]
        }
        """

        buttons = []

        if 'reply_markup_inline' in content:
            for i in content['reply_markup_inline']:

                b = {
                    "title":i['text'],
                    'action': {
                            "type": "text",
                            "text": i['text']
                        }
                }

#                 if 'callback_data' in i:
#                     b['payload'] = i['callback_data']

                if 'url' in i:
                    b['action'] =  {
                            "type": "deep_link",
                            "deep_link": i['url']
                            }



                buttons.append(b)

            del content['reply_markup_inline']

        return content, buttons


    def transform_tts(self, content):

        if 'tts' in content :
            tts_text = content['tts'].replace('\n','')
        else:
            tts_text = content['text']

        if 'audio' in content:
            del content['audio']

        tts_text = tts_text.replace('[arf]', '')

        r = {"pronounceTextType": "application/text"}
        r['items'] = [{"bubble": {"text":content['text'].replace('[arf]','')}}]
        r['pronounceText'] = tts_text


        return r


    def  transform_content(self, content):

        content, buttons = self.transform_buttons(content)
        content = self.transform_tts(content)

        # content['suggestions'] = {'buttons': buttons}

        return content


    # def transform_card(self, response):

    #     if 'card' in response:
    #         card =  {
    #               "type": "BigImage",
    #               "image_id": response['card']['image'],
    #               "title": response['card']['title'],
    #               "description": response['text']
    #         }
    #         response['card'] = card
    #     else:
    #         pass

    #     return response


    def set_context(self,user_id,data):

        name = data.get('name', '')
        value = data.get('value', '')

        if name:
            self.context.set_context(user_id, name, value)



    def response_handle(self, user_id, session_info, content, end_session = False):
        """Формирование ответа в нужном формате для Сбера"""

        if 'end_session' in content:
            end_session = content['end_session']
            del content['end_session']

        if 'set_context' in content:
            self.set_context(user_id, content['set_context'])
            del content['set_context']

        content = self.random_text(content)


        response = self.template()

        response['sessionId'] = session_info['sessionId']
        response['messageId'] = session_info['messageId']
        response['uuid'] = session_info['uuid']

        response['payload'] =  self.transform_content(content)

        session_info['device']['features'] = {
                                                "appTypes": ['CHAT_APP',
                                                'DIALOG',
                                                'EMBEDDED_APP',
                                                'WEB_APP']
                                            }

        del session_info['device']['additionalInfo']
        del  session_info['device']['deviceId']
        del  session_info['device']['deviceManufacturer']
        del  session_info['device']['deviceModel']

        # session_info['device']['devicesId'] = "123456"
        response['payload']['device'] = session_info['device']

        response['finished'] = end_session

        response['payload']['items'] =  [{'bubble': {'text': 'hello'}}]
        response['payload']['pronounceText'] =  'hello'


        return response
