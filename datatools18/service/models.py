
from conf import db as config_db
from peewee import *
from datetime import datetime

DBASE = MySQLDatabase(
    database=config_db.db_n,
    user = config_db.db_u,
    password = config_db.db_p,
    host='localhost'
)

class BaseModel(Model):
    class Meta:
        database = DBASE



class User(BaseModel):
    """
    Таблица для хранения пользователей
    """
    
    id = AutoField(unique=True)
    chat_id = CharField(max_length = 225,unique=True)
    nickname = CharField(max_length = 225, null =True)
    first_name = CharField(max_length = 225, null =True)
    last_name = CharField(max_length = 225, null =True)
    username = CharField(max_length = 225, null =True)
    phone = CharField(max_length = 225, null =True)
    birth = CharField(max_length = 100, null =True)
    subscribed = IntegerField()

    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'users'


class Loghook(BaseModel):
    """
    Таблица в которую можно записывать ошибки при отладке, используется
    например в __init__.py при вызове Exception
    """
    
    id = AutoField()
    chat_id = BigIntegerField()
    fulljson = TextField()
    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'loghook'



class Context(BaseModel):
    """
    Таблица в которой хранится текущий контекст диалога 
    для каждого пользователя
    """
    
    id = AutoField()
    user_id = IntegerField()
    memory = IntegerField()
    context = CharField(50)
    message = TextField()
    memory =  CharField(50)
    created_at = DateTimeField(default=datetime.now)
    class Meta:
        database = DBASE
        table_name = 'context'


class Feedback(BaseModel):
    """
    Таблица для хранения обращений в обратную связь бота
    """
    
    id = AutoField()
    user_id = IntegerField()
    name = CharField(250)
    phone = CharField(250)
    location = CharField(250)
    message = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'feedback'



class Content(BaseModel):
    """
        Таблица, в которой хранится контент - ключевые слова и функции для ответов
    """
    
    id = AutoField()
    ix = CharField(max_length = 300, null =True)
    sim = IntegerField()
    source = CharField(max_length = 100, null =True)
    context = CharField(max_length = 300, null =True)
    set_context = CharField(max_length = 300, null =True)
    messenger = CharField(max_length = 300, null =True)
    function = CharField(max_length = 100, null =True)
    content = CharField(max_length = 300, null =True)
    menu_inline = CharField(max_length = 1000, null =True)
    text = CharField(max_length = 1000, null =True)
    tts = CharField(max_length = 1000, null =True)
    text_var = CharField(max_length = 200, null =True)
    audio = CharField(max_length = 300, null =True)
    event_date =  DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'content'
        
        
class Logtalk(BaseModel):

    id = AutoField()
    user_id = IntegerField()
    messenger_id = IntegerField()
    content = CharField(max_length = 300, null =True)
    is_bot = IntegerField()
    ask_human = IntegerField()
    event_date =  DateTimeField(default=datetime.now)

    class Meta:
        database = DBASE
        table_name = 'log_talks'


