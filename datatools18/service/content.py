import os
import re
import json

from sklearn.feature_extraction.text import CountVectorizer


import conf.common as config
import conf.static as config_static

from service.models import Content

FIELDS_SET = ['ix','sim','audio','menu_inline','function','text','tts','text_var','source', 'content', 'set_context']

def get_content_json():

    files = os.listdir(config_static.path_to_storage)
    d,d_plus = [],[]

    for i in files:

        with open('{}/{}'.format(config_static.path_to_storage,i), 'r', encoding="utf-8") as f:
            f = f.read()
            f = re.sub('\n', '',f)
            j = json.loads(f)

            d = d + j['map']


    for i in range(len(d)):

        d[i]['source']='get_content_json'

        if type(d[i]['ix']) is list:

            for j in range(1,len(d[i]['ix'])):
                new = d[i].copy()
                new['ix'] = d[i]['ix'][j]
                d_plus.append(new)

            d[i]['ix'] = d[i]['ix'][0]

    d = d + d_plus

    return d


def get_content_map():
    """сбор доступного контента"""

    f = [
            get_content_json
        ]

    content_data = []
    for i in f:
        content_data = [*content_data, *i()]

    return content_data


def read_content_map(source):

    with open('{}/{}.json'.format(config_static.path_to_storage,source), 'r', encoding="utf-8") as f:
        f = f.read()
        f = re.sub('\n', '',f)
        j = json.loads(f)

    content_map = j['map']
    return content_map


def gen_dict(content_node, fields_set, source):
    r = []

    if 'context' not in content_node:
        content_node['context'] = [None]

    if 'sim' not in content_node:
        content_node['sim'] = config.treshold_sim * 100

    for c in  content_node['context']:

        data_dict = {'messenger':source,'context':c}

        for f in fields_set:
            data_dict[f] = content_node.get(f,None)
        # print(data_dict)
        r.append(data_dict)

    return r


def gen_content_db(content_map, source):
    content_map_response = []
    for content_node in content_map:

        r = gen_dict(content_node, FIELDS_SET, source)

        content_map_response = content_map_response + r

    return content_map_response


def save_content_db(data):

    # try:
    q = '''truncate content'''
    Content.raw(q).execute()
    # except:
    #     pass

    for row in data:
        # try:
        r = Content(**row)
        r.save()

    return 1


def content_update():
    content_map = get_content_map()
    content_map_db =  gen_content_db(content_map, 'any')
    save_content_db(content_map_db)

    return 1


class ContentDict():

    def __init__(self):
        self.type = 'words'
        self.content_map = ContentMap()



    def my_tokenizer(self, s):
	       return s.split()


    def make(self, content_map, dict_type):
        '''Cоздание словаря'''

        if dict_type == 'ngrams':
            n_range = (1,2)
            analyzer = 'char_wb'
            max_features = 1000
        else:
            n_range = (1,1)
            analyzer = 'word'
            max_features = 30000

        vectorizer = CountVectorizer(ngram_range=n_range, lowercase=True,
        analyzer=analyzer, max_features=max_features, tokenizer=self.my_tokenizer)

        vectorizer.fit(content_map)

        v = vectorizer.vocabulary_
        v ={v_key: str(v[v_key]) for v_key in v}

        return v


    def run(self,dict_type):
        '''Создание словаря n-грам'''

        content_map = self.content_map.get_content_map_db()

        content_str  = [i['ix'] for i in content_map]

        content_str = content_str + ['token1','token2','token3','token4','token5']

        dict_data = self.make(content_str, dict_type)

        self.save(dict_data, dict_type)

        return 'dict saved {} {}'.format(len(content_map), str(dict_data))


    def filename(self,dict_type):
        """определение названия файла со словарем токенов"""

        if dict_type == 'ngrams':
            fn = 'dict_nrgams_dict_w123.json'
        else:
            fn = 'dict_dict_w1.json'

        return fn


    def open(self, dict_type):
        """словарь с н-граммами"""

        fn = self.filename(dict_type)
        char_dictionary = json.loads(open('{}/{}'.format(config_static.path_to_files,fn)).read())

        return char_dictionary


    def save(self,dict_data, dict_type):

        fn = self.filename(dict_type)

        fp = open('{}/{}'.format(config_static.path_to_files, fn), 'w')
        fp.write(json.dumps(dict_data))
        fp.close()

        return True



class ContentMap():

    def __init__(self):
        pass


    def modify_filter_context(self,context,context_list,dict_type):
        '''обработка контекстов, которые содержат id - добавление такого же контекста без id'''
        if dict_type == 'words':
            filter_context = "context in ('{}')".format("','".join(['any',*context_list]))

        else:
            filter_context = "context in ('{}')".format("','".join(context_list))

        return filter_context


    def get_content_map_db(self, context = 'dict', messenger = [], dict_type='words'):
        """сбор доступного контента из БД"""

        if context == 'dict':
            filter_context = ""

        else:
            if context in ['drop',None,'round_reset','exit']:
                filter_context = "(context is null or context in ('any'))"

            else:
                context_list = [context]
                filter_context = self.modify_filter_context(context,context_list,dict_type)


        if len(messenger):
            filter_messenger = "messenger in ('{}')".format("','".join(['any',messenger]))
        else:
            filter_messenger = ""


        sql_filter = [i for i in [filter_messenger, filter_context] if len(i) > 0]

        q = '''
                select
                    id, ix, sim, text, tts, text_var, context, set_context, function, content, menu_inline, audio
                from content
            '''
        if sql_filter:
            q = q + '''
                where {}
            '''.format(' and '.join(sql_filter))

        cm = Content.raw(q).dicts()
        cm = [i for i in cm]

        return cm
