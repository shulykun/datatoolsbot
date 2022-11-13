
import os
import re
import json

from gensim import corpora, models, similarities
from gensim.similarities import MatrixSimilarity

import conf.tokens as config_tokens
import conf.common as config
import conf.static as config_static

from service.models import *
from service.content import ContentDict, ContentMap

os.environ["PYTHONIOENCODING"] = "utf-8"


class SearchEngine():

    def __init__(self):
        self.window = [1,2]
        self.stopwords = config_tokens.nltk_stopwords
        self.content_dict = ContentDict()
        self.content_map = ContentMap()

    def my_tokenizer(self, s):
	       return s.split()


    def modify_search_ngrams(self, sims, query, context, messenger):
        '''при некоторых значениях воронки ищем по n-граммам, пока отключено'''

        return sims
        # if len(sims) == 0:
        #
        #     if 'riddle' in context or 'competition_active' in context:
        #
        #         char_dictionary = self.open_dict('ngrams')
        #
        #         content_map = self.get_content_map_db(context, messenger, 'ngrams')
        #
        #         sims = self.get_similar_words(query, char_dictionary, content_map, 'ngrams')
        #         return sims
        #
        # return sims


    def handle_request(self, query, d_type, context = [], messenger = ''):
        """"""
        response = []

        content_map  = self.content_map.get_content_map_db(context, messenger)

        if len(content_map):
            char_dictionary = self.content_dict.open(d_type)
            sims = self.get_similar_words(query, char_dictionary, content_map, d_type)
            # sims = self.modify_search_ngrams(sims, query, context, messenger)

            if len(sims) > 0:
                return sims
            else:
                sims = [i for i in content_map if i['ix'] == '*']
                if len(sims) > 0:
                    return sims

        return response


    def get_similar_words(self, query_str, char_dictionary, content_map, d_type):
        """
        Получение списка похожих слов по близости с заданым окном
        """

        # content_str, content_id = zip(*content_list.items())
        content_str = [i['ix'] for i in content_map]

        content_vector, query_vector = self.transform_corpus(query_str, content_str, char_dictionary, d_type)

        index = MatrixSimilarity(content_vector, num_features=len(char_dictionary))

        sims = index[query_vector]


        sims_sorted = sorted(enumerate(sims), key=lambda item: -item[1])

        response = []
        for s in sims_sorted:
            c = content_map[s[0]]

            sim_treshold = c['sim'] / 100
            if s[1] >= sim_treshold:

                c['sim'] = s[1]

                response.append(c)

                return response

        return response


    def transform_corpus(self, query_str, content_str, char_dictionary, d_type):
        """
            преобразование вопроса и вариантов ответов в вектор
            по заранее сохраненному словарю
        """

        dictionary = corpora.Dictionary([[i] for i in char_dictionary])

        if d_type == 'ngrams':
            content_vector = [dictionary.doc2bow(self.get_token_chars(text, windows = self.window)) for text in content_str]
            #corpus_w = [self.get_token_chars(text, windows = self.window) for text in offers_txt]
            query_vector = dictionary.doc2bow(self.get_token_chars(query_str, windows = self.window))

        else:
            content_vector = [dictionary.doc2bow(self.get_tokens(text)) for text in content_str]
            #corpus_w = [self.get_token_chars(text, windows = self.window) for text in offers_txt]
            query_vector = dictionary.doc2bow(self.get_tokens(query_str, char_dictionary))

        return content_vector, query_vector


    def get_tokens(self, query_str, dictionary = {}):
            """преобразование текста в набор слов"""
            a = query_str.split()

            n = 0
            a_plus = []
            if dictionary:
                for i in a:
                    if i not in dictionary:
                        n+=1
                        a_plus.append('token{}'.format(n))

            a = a + a_plus
            # print(a)
            return set(a)


    def get_token_chars(self, text, windows):
        """преобразование текста в набор н-грам"""
        v = []
        for w in windows:
            for i in range(0, len(text)):
                start = i
                end = i + w
                text_to_add = text[start:end]
                if len(text_to_add) == w:
                    v.append(text_to_add)
        return v
