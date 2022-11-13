# -*- coding: utf-8 -*-
from flask import Flask,  request, session, g, jsonify, make_response

import os
import telebot
import traceback

import conf.common as config

from receiver.telegram import TelegramMessage
from content.process import processTg
from service.models import *
from service.tonque.telegram import TonqueTg

tg_message = TelegramMessage()
bot = telebot.TeleBot(config.tg_token)

app = Flask(__name__)
app.config.from_object(__name__)

## Поместить сюда название таблицы из service.models, чтобы таблица создалась в БД
DBASE.create_tables([User,Loghook,Context,Feedback,Logtalk,Content], safe=True)


@app.route('/hook/', methods=['POST'])
def hook():
    """Прием веб хуков от телеграма"""

    if request.headers.get('content-type') == 'application/json':

        input_message = tg_message.convert(request.json)

        processor = processTg(TonqueTg())
        processed = processor.response(input_message)

        json_stored = Loghook(fulljson=str(request.json), chat_id = 1)
        json_stored.save()

    else:
        processed = request.headers.get('content-type')

    return str(processed)



@app.route('/content_update')
def route_content_update():
    """
        Ссылка для обновление базы контента - делать всегда после обновлений в common.json
        https://datatools18.roborumba.com/content_update
    """
    from service.content import ContentDict, content_update

    try:

        content_update()

        c = ContentDict()
        x = c.run('words')

    except Exception as e:
        tb = traceback.format_exc()
        x = str(e) + ' ' + str(tb)
    return str(x)




@app.route('/vector_search')
def vector_search():
    """
        Ссылка для визуальной проверки поиска по слову
        Например:
        https://datatools18.roborumba.com/vector_search?q=как%20переводится%20привет
    """
    from service.search import SearchEngine
    from service.semantic import TextProcessor

    searcher = SearchEngine()
    textProcessor = TextProcessor()


    s = request.args.get('q')
    s_norm = textProcessor.normalise(s)

    try:
        x = searcher.handle_request(s_norm, d_type='words',context='')
    except Exception as e:
        x = str(traceback.format_exc()) + str(e)

    return 'входящий запрос:{} нормализованный запрос: {} ранжирование ответов: {}'.format(s, s_norm, str(x))



@app.route('/')
def index_page():
    """Заглушка на главной странице"""
    return "hello, it's datatool bot"


@app.route('/me/')
def me():
    """проверка имени бота"""
    user = bot.get_me()
    username = user.username
    return username


@app.route('/set_hook/')
def set_hook():
    """установка адреса вебхука телеграма"""
    try:
        bot.set_webhook(url=config.tg_hook)
        r ='hook set to {}'.format(config.tg_hook)
    except Exception as e:
        r = str(e)
    return r


@app.teardown_request
def _db_close(exc):
    if not DBASE.is_closed():
        DBASE.close()


if __name__ == '__main__':
    app.run(debug=True)
