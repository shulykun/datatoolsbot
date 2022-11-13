from service.models import Feedback
from service.context import ContextProcess
from content.replics import Replics
# from emailsender import EmailSender



class FeedbackChat:
    def __init__(self, medium):
        replics = Replics()
        self.replics = replics.set_class(medium)
        self.context = ContextProcess()


    def new_chat(self, chat_id):
        fb = Feedback(user_id=chat_id)
        fb.save()
        return fb.id


    def feedback_start(self,user_id, meaning, text, text_raw):

        new_chat_id = self.new_chat(user_id)
        response = self.replics.feedback_start(new_chat_id)

        return response


    def open_last_chat(self, chat_id):
        fb =  Feedback.select().where((Feedback.user_id == chat_id)).order_by(Feedback.id.desc()).dicts()
        if len(fb):
            fb = fb.get()
        return fb


    def update_chat(self, id, fields):
        query = Feedback.update(**fields).where(Feedback.id == id)
        query.execute()
        return query


    def text_add(self, chat_id, message_id, text, text_raw):

        last_chat = self.open_last_chat(chat_id)
        self.update_chat(last_chat['id'], {'message':text_raw})

        return self.replics.feedback_confirm()


    # def get_username(self, chat_id):
    #     fb =  User.select().where((User.id == chat_id)).get()
    #     if fb.username:
    #         un = '(ник: @{})'.format(fb.username)
    #     else:
    #         un = ''
    #     return un
