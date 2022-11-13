from service.models import *
# from semantic import TextProcessor
from datetime import datetime, timedelta

class ContextProcess:

    def __init__(self):
        """Constructor"""
        pass
        # self.textProcessor = TextProcessor()


    def add_context(self, chat_id, text):
        """добавление контекста к словам на основе предыдущих значений"""
        lf =  self.last_context(chat_id)

        return text


    def set_context(self, chat_id, context, message_text, memory = 2):
        """Сохранение состояния последней беседы. memory: 1 на одну реплику, 2 долгая."""

        if context in ['ask_start','competition_ask_restart','sparring_ask_restart','sparring_complete']:
            memory = 1

        context = Context(user_id=chat_id, context=context, message = message_text, memory = memory)
        context.save()

        return 1


    def drop_context(self, id):
        q = '''
            DELETE FROM context
            WHERE id = {}'''.format(id)

        r = Context.raw(q)
        r.execute()
        return 1


    def last_context(self, chat_id, context_name=None, days=1):
        """определяем была ли уже воронка с фильтром и смотрим какие данные висят в ней"""

        date_from = datetime.strftime(datetime.now() - timedelta(days),'%Y-%m-%d')

        r = {'context':context_name, 'message':None}

        sql_filter = ""
        if context_name:
            sql_filter = "and context = '{}'".format(context_name)

        q = """
                SELECT id, message, context, memory
                FROM context
                WHERE user_id = {chat_id}
                and created_at > '{date_from}' {sql_filter}
                ORDER BY id DESC
            """.format(chat_id=chat_id, date_from=date_from, sql_filter=sql_filter)

        last_context = [i for i in Context.raw(q).dicts()]

        if len(last_context):
            if last_context[0]['memory'] in [1,'1']:
                self.set_context(chat_id, 'drop', '')

            return last_context[0]
        else:
            return r
