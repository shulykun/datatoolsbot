import random

replic_vars = {
    "i_silent":"Всё, молчу",
    "how_are_you":"По разному - то штиль, то шторм",
    "no_angry":"Пожалуйста, давай не будем ругаться. Если что-то не понравилось, оставь отзыв.",
    "no_content":"С эим ничем не могу помочь. Чтобы выйти из навыка, скажи Алиса, хватит.",
    "glad_you_like":")) Я рад что тебе нравится",
    "glad_you_like_2":"Пожалуйста!",
    "bye-bye":"👋 Пока-пока!",
    "hello":["👋 Здорово!","👋 Привет!"],
    "hello_tts":"Привет",
    "what_you_can":[
        "Я умею ..."
        ],
    "help":[
        "Вот мои основные команды: ..."
        ],
    "help_tts":[
        "Вот мои основные команды: ..."
        ],
    "not_defined":[
        'Извини, я не распознал твой вопрос.',
        'Тут, я не знаю как ответить.'
    ]
}


def get_replic_var(key):

    text = replic_vars[key]
    if type(text) == list:
        text = random.choice(text)

    return text
