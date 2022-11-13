#Разбинение на элементы поступающего текста
import emoji
import json
import pymorphy2
import re
import conf.tokens as dict_input

class TextProcessor:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        pass


    def check_text(self, t):
        check_text = re.search('[A-Za-zА-Яа-я0-9]', t)
        return check_text


    def get_content(self, message):
        """Извлекаем из сообщения контент """

        text, text_raw, emoji, photo_id = '', '', False, None

        if message['text']:
            text_raw = message['text']

            if self.check_text(text_raw):
                text = self.normalise(text_raw)

            emoji, text_raw = self.check_emoji(text_raw)

        return text, text_raw, emoji


    def add_bitoken(self, x):

        for i in x:
            yield i

        for i in range(len(x)-1):
            yield '{}_{}'.format(x[i],x[i+1])



    def detect_url(self, text):

        f = re.search('https://[^\s]+', text)
        if f:
            return f.group(0)
        else:
            return None


    # def normalise(self, text):
    #     """Приведение формы к единственному числу именительному падежу"""
    #     #phrase_norm = []
    #
    #     text_clean = re.sub('[^\w\s-]', '', text)
    #     text_clean = [i.lower().strip() for i in text_clean.split(' ')]
    #
    #         # if part not in config_tokens.words_stoplist:
    #     for part in text_clean:
    #         if part not in config_tokens.normalize_exclude:
    #             #phrase_norm.append(self.morph.parse(part)[0].normal_form)
    #             yield self.morph.parse(part)[0].normal_form
    #         else:
    #             #phrase_norm.append(part)
    #             yield part
    #
    #     url = self.detect_url(text)
    #     if url:
    #         yield url

    def normalise(self, text):
        """Приведение формы к единственному числу именительному падежу"""

        phrase_norm = []
        text_clean = re.sub('[^\w\s-]', '', text)

        url = self.detect_url(text)

        if url:
            text_clean = '{} {}'.format(text_clean,url)

        text_clean = [p.lower().strip() for p in text_clean.split(' ') if p.lower().strip()]

        for part in text_clean:
            if part not in dict_input.normalize_exclude:
                phrase_norm.append(self.morph.parse(part)[0].normal_form)
            else:
                phrase_norm.append(part)

        response = ' '.join(self.add_bitoken(phrase_norm))

        return response


    def show_emoji(self, text):
        """Вывод эмодзи"""
        text = emoji.emojize(text)

        return text


    def check_emoji(self, text):
        """Проверка на эмодзи"""
        js_text = text

        j = False

        if len(text) > len(text.encode('windows-1251', 'ignore')):

            js_text = json.loads('["{}"]'.format(text))[0]

            j = [t for t in js_text if t in emoji.UNICODE_EMOJI]

            js_text = emoji.demojize(js_text)

        return j,js_text


    def define_positive(self, text):
        # return 1

        """Определяем тональность фразы 0 негатив 1 позитив 3 далее 2 не определено"""

        ## Четкое выражение с одним словом
        positive_list =  ['да', 'давай', 'ага', 'угу', 'ок', 'согласен', 'da','отправить']
        negative_list = ['отмена', 'нет', 'не надо', 'cancel']
        more_list = ['ещё', 'дальше', 'следующий', 'далее','ближайший']

        response = 2

        for phrases_list in [[positive_list, 1], [negative_list, 0], [more_list, 3]]:

            phrases_list_restricted = ['^{}$'.format(e) for e in phrases_list[0]]
            phrases = '({})'.format('|'.join(phrases_list_restricted))

            if re.search(phrases, text):
                response = phrases_list[1]
                break

        if response == 2:

            ## Нечеткое выражение - содержит ключевое слово и еще пару слово
            if len(text.split(' ')) < 4:

                for phrases_list in [[positive_list, 1], [negative_list, 0], [more_list, 3]]:

                    phrases_list_spaces = ['{}(,|\.|\s)'.format(e) for e in phrases_list[0]]

                    phrases = '({})'.format('|'.join(phrases_list_spaces))

                    if re.search(phrases, text):
                        response = phrases_list[1]
                        break



        return response
