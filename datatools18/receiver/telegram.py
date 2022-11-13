
# update.callback_query
# update.message
# update.message.text
# update.message.from_user.first_name
# update.message.from_user.id
# update.message.from_user.last_name
# update.message.from_user.phone
# update.message.chat.id
# update.callback_query.message.chat.id
# update.callback_query.data

class TelegramMessage:

    def message_template(self):

        t = {
                "user_id":0,
                "is_bot":"false",
                "first_name":"Telegram_User",
                "last_name":"Telegram_User",
                "language_code":"ru",
                "text":"",
                "callback_data":"",
                "session":None
            }

        return t


    def convert(self,input_message):
        m = self.message_template()

        # print('input_message',input_message)

        if 'callback_query' in input_message:
            from_info = input_message['callback_query']['from']
            message = input_message['callback_query']['message']

            m["callback_data"] = input_message['callback_query']['data']

        else:
            from_info = input_message['message']['from']
            message = input_message['message']

        names_dict = {'id':'user_id','first_name':'first_name', 'last_name':'first_name','username':'username'}

        for i in ['id','first_name','last_name','username']:
            m[names_dict[i]] = from_info.get(i,'')

        m["text"] = message['text']

        return m
#
# {'update_id': 675792046,
# 'message':
#     {
#         'message_id': 6574,
#         'from':
#             {'id': 79711951, 'is_bot': 'false', 'first_name': 'Vadim', 'last_name': 'Shulginov', 'username': 'shulykun', 'language_code': 'ru'},
#         'chat':
#             {'id': 79711951, 'first_name': 'Vadim', 'last_name': 'Shulginov', 'username': 'shulykun', 'type': 'private'},
#         'date': 1532835342,
#         'text': 'привет'
#     }
# }
#
#     def callback_template(self):
#         t = {"update_id":10,
#             "callback_query":{
#                 "id":"342360226798281673",
#
#                  "from": {"id":0,"is_bot":
#                           'false',
#                        "first_name":"Vadim",
#                         "last_name":"Shulginov",
#                        "username":"shulykun",
#                         "language_code":"ru"
#                     },
#                   "message":{"message_id":0,
#                      "from":{"id":0,
#                             "is_bot":'true',
#                             "first_name":"FN",
#                              "username":"syngamebot"
#                          },
#                          "chat":{"id":0,
#                                  "first_name":"Vadim",
#                                  "last_name":"Shulginov",
#                                  "username":"shulykun",
#                                  "type":"private"},
#                          "date":0,
#                         "text":"text",
#                     },
#                   "chat_instance":"4929982818428841915",
#                   "data":"score_total"
#             }
#         }
#         return t
