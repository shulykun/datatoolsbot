from service.context import ContextProcess
from content.replics import Replics
from service.models import User, Loghook

class Smalltalk:


    def __init__(self, medium):
        self.medium = medium
        replics = Replics()
        self.replics = replics.set_class(medium)
        self.context = ContextProcess()


    def not_defined(self, user_id, text, text_raw, context=''):
        """Генерим ответ  если тема не найдена"""

        json_stored = Loghook(fulljson=str([text, text_raw, context]), chat_id = 505)
        json_stored.save()

        response = self.replics.not_defined(text)

        return response


    def drop(self, user_id, meaning, text, text_raw):
        """Выход в главное меню"""

        response = self.replics.drop()

        return response


    def help(self, user_id, meaning, text, text_raw):
        """Помощь"""

        response = self.replics.help()

        return response
