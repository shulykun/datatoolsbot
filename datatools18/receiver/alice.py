class AliceMessage:

    def __init__(self):
        pass


    def message_template(self):

        t = {
                "user_id":0,
                "is_bot":"false",
                "first_name":"Alice_User",
                "last_name":"Alice_User",
                "language_code":"ru",
                "text":"",
                "session":"",
                "callback_data":""
            }

        return t


    def convert(self,input_message):

        # print('input_message',input_message)

        m = self.message_template()

        m["user_id"] = input_message['session']['user_id']
        m["last_name"] = input_message['session']['session_id']

        if "original_utterance" in input_message['request']:
            m["text"] = input_message['request']['original_utterance']

        m["session"] = input_message['session']
        if 'payload' in input_message['request']:
            m["callback_data"] = input_message['request']['payload']

        if m["text"] == '':
            m["text"] = 'рестарт'

        return m
