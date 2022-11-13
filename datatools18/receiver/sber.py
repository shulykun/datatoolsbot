class SberMessage:
    
    def __init__(self):
        pass


    def message_template(self):

        t = {
                "user_id":0,
                "session":{},
                "device":{},
                "language_code":"ru",
            
                "first_name":"Sber",
                "last_name":"",
                
                "text":"",
                "character":"",
                "callback_data":""
            }

        return t


    def convert(self,input_message):


        m = self.message_template()

        m["user_id"] = input_message['uuid']['userId']
        m["last_name"] = input_message['sessionId']

        m["text"] = input_message['payload']['message']['original_text']
                        
        
        m["character"] =  input_message['payload']['character']['id']
        
        m["session"] = {
                        "sessionId": input_message['sessionId'],
                        "messageId": input_message['messageId'],
                        "uuid": input_message['uuid'],
                        "device":input_message['payload']['device']
            
        }
                    
#         if 'payload' in input_message['request']:
#             m["callback_data"] = input_message['request']['payload']

        if m["text"] == '':
            m["text"] = 'рестарт'

        return m