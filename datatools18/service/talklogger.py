from threading import Thread


import conf.common as config

from service.models import Logtalk
from service.ga import gaTracker

class TalkLogger:
    def __init__(self):
        self.tracker = gaTracker()


    def asyncStoreInput(self, user_id, messenger_id, content, context='none', function='not_defined'):
        Thread(target=self.storeInputComplex, args=(user_id, messenger_id, content, context, function)).start()
        return 1


    def asyncStoreOutput(self, user_id, messenger_id, content):
        # content = self.modify_content(content)
        Thread(target=self.storeOutputComplex, args=(user_id, messenger_id, content)).start()
        return 1

    def storeInputComplex(self, user_id, messenger_id, content, context, function):
        # self.storeInput(user_id, messenger_id, content)
        self.tracker.storeInput(user_id, messenger_id, content, context, function)


    def storeOutputComplex(self, user_id, messenger_id, content):
        # self.storeOutput(user_id, messenger_id, content)
        self.tracker.storeOutput(user_id, messenger_id, content)



    def storeInput(self, user_id, messenger_id, content):
        data = {
                'user_id':user_id,
                'messenger_id':messenger_id,
                'is_bot':0,
                'ask_human':0,
                'content':content
                }
        stored = Logtalk(**data)
        stored.save()


    def storeOutput(self, user_id, messenger_id, content, ask_human=0):
        data = {
                'user_id':user_id,
                'messenger_id':messenger_id,
                'is_bot':1,
                'ask_human':0,
                'content':content
                }
        stored = Logtalk(**data)
        stored.save()
