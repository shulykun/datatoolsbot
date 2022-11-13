
from service.context import ContextProcess
from service.models import User

class UserProcessor:
    def __init__(self):
        self.context = ContextProcess()


    def get_user_id(self, message, chat_id):
        user_saved = self.user_update(message, chat_id)
        user_id  = user_saved.id

        user_id_host = self.get_user_connection(user_id)


        if user_id_host:
            return user_id_host
        else:
            return user_id

    def user_update(self, message, chat_id):
        """Сохранение пользователя"""
        try:
            user = User.get(User.chat_id == chat_id)

        except User.DoesNotExist:

            dict_user = {
                'chat_id':chat_id,
                'first_name':message.get('first_name', '-'),
                'last_name':message.get('last_name', '-'),
                'username': message.get('username', '-'),
                'phone':message.get('phone', '-'),
                'subscribed':0
            }
            user = User.create(**dict_user)

        except AttributeError:
            return 'Wrong Attribute'

        return user
