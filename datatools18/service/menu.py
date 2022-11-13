# import json
from service.models import *
from telebot import types

class menuChat:

    def __init__(self):
        """Constructor"""
        pass



    def genInlineButtons(self, inline_buttons):
        """Генерация inline-кнопок в меню"""

        keyboard = types.InlineKeyboardMarkup()

        buttons = []
        for ib in inline_buttons:
            # if type(ib) == dict:
            buttons.append(types.InlineKeyboardButton(**ib))
            # else:
            #     row = []
            #     for x in ib:
            #         item  = types.InlineKeyboardButton(**x)
            #         row.append(item)
            #     buttons.append(row)

        keyboard.add(*buttons)

        return keyboard


    def genButtons(self, menu_content):
        """составление меню"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        buttons = []
        for b_content in menu_content:
            buttons.append(types.KeyboardButton(b_content))
        keyboard.add(*buttons)

        return keyboard
