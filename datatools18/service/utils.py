import re
# from logic.players import Player
# players = Player()
TRANS_DICT = {
    'r':'р',
    'ɛ': 'э',
 'l': 'л',
 'd': 'д',
 'ə': 'е',
 'i': 'и',
 'm': 'м',
 'a': 'а',
 'ɪ': 'и',
 'z': 'з',
 'ɹ': 'р',
 'w': 'в',
 'ɒ': 'о',
 'n': 'н',
 't': 'т',
 's': 'с',
 'p': 'п',
 'æ': 'э',
 'ð': 'з',
 'o': 'о',
 'ɡ': 'г',
 'v': 'в',
 'k': 'к',
 'ɜ': 'ё',
 'ʉ': 'у',
 'ʌ': 'а',
 'ʃ': 'ш',
 'ŋ': 'н',
 'ʍ': 'уэ',
 'ʊ': 'у',
 'b': 'б',
 'e': 'е',
 'f': 'ф',
 'θ': 'ф',
 'ɔ': 'о',
 'ɑ': 'а',
 'ʒ': 'ж',
 'h': 'х',
 'u': 'у',
'ɝ':'о',
'ː':'',
'ʤ':'дж',
'ʧ':'тч',
'j':'й'}


NUM_ADJ = {
        '1':'первый',
        '2':'второй',
        '3':'третий',
        '4':'четвертый',
        '5':'пятый',
        '6':'шестой',
        '7':'седьмой',
        '8':'восьмой',
        '9':'девятый',
        '10':'десятый',
        '11':'одиннадцатый',
        '12':'двенадцатый',
        '13':'тринадцатый',
        '14':'четырнадцатый',
        '15':'пятнадцатый',
        '16':'шестнадцатый',
        '17':'семнадцатый',
        '18':'восемнадцатый',
        '19':'девятнадцатый',
        '20':'двадцатый',
        '30':'тридцатый',
        '40':'сороковой',
        '50':'пятидесятый',
        '60':'шестидесятый',
        '70':'семидесятый',
        '80':'восьмидесятый',
        '90':'девяностый',
        '100':'сотый',
        '200':'двухсотый',
        '300':'трехсотый',
        '400':'четырехсотый',
        '500':'пятисотый',
        '600':'шестисотый',
        '700':'семисотый',
        '800':'восьмисотый',
        '900':'девятисотый',
        '1000':'тысячный',
        '000':'тысячный'
    }

NUM_NOUN = {
        '1':'один',
        '2':'два',
        '3':'три',
        '4':'четыре',
        '5':'пять',
        '6':'шесть',
        '7':'семь',
        '8':'восемь',
        '9':'девять',
        '10':'десять',
        '11':'одиннадцать',
        '12':'двенадцать',
        '13':'тринадцать',
        '14':'четырнадцать',
        '15':'пятнадцать',
        '16':'шестнадцать',
        '17':'семнадцать',
        '18':'восемнадцать',
        '19':'девятнадцать',
        '20':'двадцать',
        '30':'тридцать',
        '40':'сорок',
        '50':'пятьдесят',
        '60':'шестьдесят',
        '70':'семьдесят',
        '80':'восемьдесят',
        '90':'девяносто',
        '100':'сто',
        '200':'двести',
        '300':'триста',
        '400':'четыреста',
        '500':'пятьсот',
        '600':'шестьсот',
        '700':'семьсот',
        '800':'восемьсот',
        '900':'девятьсот',
        '1000':'тысяча',
        '2000':'две тысячи',
        '3000':'три тысячи',
        '4000':'четыре тысячи',
        '5000':'пять тысяч',
        '6000':'шесть тысяч',
        '7000':'семь тысяч',
        '8000':'восемь тысяч',
        '9000':'девять тысяч',
        '10000':'десять тысяч',
        '11000':'одиннадцать тысяч',
        '12000':'двенадцать тысяч',
        '13000':'тринадцать тысяч',
        '14000':'четырнадцать тысяч',
        '15000':'пятнадцать тысяч'
    }

NUM_FORM = {
     'одно':'si',
     'один':'si',
     'два':'sr',
     'три':'sr',
     'четыре':'sr'
    }


def join_enumeration(data):
    if len(data) > 1:
        term_vars_str = '{} или {}'.format(', '.join(data[:-1]), data[-1])
    else:
        term_vars_str = data[0]
    return term_vars_str

def is_english(term):
    s = 'abcdefghefijkloqwrtyupzxsvx'

    s_en = [i for i in term if i in s]

    if len(s_en) > len(term) - 5:
        return True
    else:
        return False


def token_form(token):
    if token in NUM_FORM.keys():
        return NUM_FORM[token]
    else:
        return 'mr'


def num2text_noun(input_num):

    r = []
    input_len = len(input_num)

    for j in range(input_len):
        a = input_num[j:]
        if a in NUM_NOUN.keys():
            a_ = NUM_NOUN[a]
            r.append(a_)
            break

    for i in range(input_len-j+1,input_len+1):
        x =  input_num[-i][0] + '0' * (i-1)
        if x in NUM_NOUN.keys():
            x_ = NUM_NOUN[x]
            r.append(x_)

    r.reverse()

    return r


def num2text_adj(input_num):

    r = []
    input_len = len(input_num)

    for j in range(input_len):
        a = input_num[j:]
        if a in NUM_ADJ.keys():
            a_ = NUM_ADJ[a]
            r.append(a_)
            break

    for i in range(input_len-j+1,input_len+1):
        x =  input_num[-i][0] + '0' * (i-1)
        if x in NUM_NOUN.keys():
            x_ = NUM_NOUN[x]
            r.append(x_)

    r.reverse()

    return r


def get_token_form(token):
    if token in NUM_FORM.keys():
        return NUM_FORM[token]
    else:
        return 'mr'


def get_th(num, prev_number):

    num = num-2

    DICT_TH =  [
            {'si':'тысяча', 'sr':'тысячи','mr':'тысяч'},
            {'si':'миллион', 'sr':'миллиона','mr':'миллионов'},
            {'si':'миллиард', 'sr':'миллиарда','mr':'миллиардов'}
           ]

    if num >=0:
        return DICT_TH[num][get_token_form(prev_number)]
    else:
        return ''



def num2text_noun_adj_t(input_num):

    r = []
    input_num_l = format(int(input_num), ',').split(',')
    size = len(input_num_l)
    for i in input_num_l:

        if size == 1:
            t = num2text_adj(i)
        else:
            t = num2text_noun(i)
        r = [*r,*t, get_th(size,  t[-1])]

        size -= 1
    r = ' '.join(r).strip().replace('один тыс','одна тыс').replace('два тыс','две тыс').split()
    return r






def score_form(input_num):

    try:
        num_text_list = num2text_noun(str(input_num))
        if num_text_list[-1] == 'один':
            num_text_list[-1] = 'одно'

        num_text_last = num_text_list[-1]

        token_form = get_token_form(num_text_last)

        word_dict = {
            'si':'очко',
            'sr':'очка',
            'mr':'очков'
        }

        word_score_list = num_text_list + [word_dict[token_form]]

        word_score = '{word_score} {score_form}'.format(word_score = input_num,  score_form = word_score_list[-1])
        word_score_tts = ' '.join(word_score_list)

        return word_score, word_score_tts

    except:
        return str(input_num) + ' очков', str(input_num) + ' очков'



def rank_form(input_num):

    try:
        num_text_list = num2text_noun(str(input_num))

        num_text_last = num_text_list[-1]
        token_form = get_token_form(num_text_last)

        if num_text_last == 'один':
            num_text_last = 'одну'

        elif num_text_last == 'два':
            num_text_last = 'две'

        num_text_list[-1] = num_text_last


        word_dict = {
            'si':'позицию',
            'sr':'позиции',
            'mr':'позиций'
        }

        word_score_list = num_text_list + [word_dict[token_form]]

        word_score = '{word_score} {score_form}'.format(word_score = input_num,  score_form = word_score_list[-1])
        word_score_tts = ' '.join(word_score_list)

        return word_score, word_score_tts

    except:

        return str(input_num) + ' позиций', str(input_num) + ' позиций'



def games_form(input_num):

    try:
        num_text_list = num2text_noun(str(input_num))

        num_text_last = num_text_list[-1]
        token_form = get_token_form(num_text_last)

        if num_text_last == 'один':
            num_text_last = 'одну'

        elif num_text_last == 'два':
            num_text_last = 'две'

        num_text_list[-1] = num_text_last

        word_dict = {
            'si':'игру',
            'sr':'игры',
            'mr':'игр'
        }

        word_score_list = num_text_list + [word_dict[token_form]]

        word_score = '{word_score} {score_form}'.format(word_score = input_num,  score_form = word_score_list[-1])
        word_score_tts = ' '.join(word_score_list)

        return word_score, word_score_tts

    except:
        return str(input_num) + ' игр', str(input_num) + ' игр'



def place_form(input_num):

    subject = 'место'

    try:
        num_text_list = num2text_noun_adj_t(input_num)
        last_token = num_text_list[-1]
        if last_token == 'третий':
            last_token = 'третье'

        else:
            last_token = last_token[:-2] + 'ое'

        word_score_list = num_text_list[:-1] + [last_token] + [subject]

        word_score = '{} {}'.format(input_num,  subject)
        word_score_tts = ' '.join(word_score_list)

        return word_score, word_score_tts

    except:
        return str(input_num) + ' {}'.format(subject), str(input_num) + ' {}'.format(subject)


def words_form_d(input_num):

    input_num = str(input_num)

    word_form = {
        '1':'si',
        '2':'sr',
        '3':'sr',
        '4':'sr'
    }

    word_dict = {
        'si':'слово',
        'sr':'слова',
        'mr':'слов'
    }

    wf = 'mr'

    last_num = input_num[-1]
    if last_num in ['1','2','3','4']:
        if len(input_num)> 1:
            if input_num[-2] != '1':
                wf = word_form[last_num]
        else:
            wf = word_form[last_num]


    wf = word_dict[wf]

    word_score = '{} {}'.format(input_num, wf)
    # word_score_tts = '{} {}'.format(input_num,  wf)

    return word_score


def remove_double_words(text):



    ts = text.split(' ')
    r = [ts[0]]
    for i  in range(1, len(ts)):
        if ts[i] != ts[i-1]:
            r.append(ts[i])

    return ' '.join(r)


def modify_name(text_raw):
    # text_raw = text_raw.lower().strip().capitalize()
    a = text_raw.lower()

    for i in ['алиса меня зовут', 'меня зовут', 'мое имя', 'первый игрок']:
        a = a.replace(i,'')

    if 'зовут' in a:
        a = [i for i in a.split('зовут') if i]
        a = a[-1]

    if 'а меня' in a:
        a = a.split('а меня')
        a = a[0]

    if ' и ' in a:
        a = a.split(' и ')
        a = a[0]


    a = remove_double_words(a)

    a = a.strip().capitalize()

    return a


def transliterate_phonetic(term):
#     print(term)
    data = [TRANS_DICT.get(i, '') for i in term]
    return ''.join([d for d in data if d])



def is_sentence(s):

    if s[-1] == '.' and s[0].lower() != s[0]:
        return True

    if s[-1] == '.' and s[2].lower() != s[2]:
        return True


def is_russian(s):

    if re.search('[А-Яа-я]+',s):
        return True
    else:
        return False


def define_num(text):

    a = {
        'первый':0,
        'второй':1,
        'третий':2,
        'четвертый':3,
        'номер_один':0,
        'номер_два':1,
        'номер_три':2,
        'номер_четыре':3,
        'вариант_один':0,
        'вариант_два':1,
        'вариант_три':2,
        'вариант_четыре':3,
        '1':0,
        '2':1,
        '3':2,
        '4':3,
        'номер_1':0,
        'номер_2':1,
        'номер_3':2,
        'номер_4':3,
        'последний':100
    }

    t = text.split(' ')

    for i in t:
        if i in a:
            return a[i]

    return -1





def modify_name(text_raw):
    text_raw = text_raw.replace('меня зовут','').replace('мое имя','').strip()
    return text_raw


# def modify_text_with_gender(text, gender):
#
#     if gender not in ['m','w']:
#
#         # print('modify_text_with_gender',gender)
#
#         gender = 'm'
#
#     f = re.findall('\[[^[^\]]+\]',text)
#
#     for i in f:
#
#         r = "("+gender+":)([^\[^\],]+)"
#
#         a = re.search(r,i)
#         if a:
#             text  = text.replace(i, a.groups()[1])
#
#     return text

# def change_gender_uid(func):
#     def inner(*args, **kwargs):
#
#         user_id = args[0]
#         gender = players.get_gender_from_user(user_id)
#         text = func(*args, **kwargs)
#         text = modify_text_with_gender(text, gender)
#
#         return text
#
#     return inner


#
# def d_c_gender_name(func):
#     """"""
#
#     def inner(*args, **kwargs):
#
#         name = args[0]
#         gender = players.get_gender_from_name(name)
#         text = func(*args, **kwargs)
#         text = modify_text_with_gender(text, gender)
#
#         return text
#
#     return inner

#
# def change_gender_name(text,name):
#
#     # print('change_gender_name',name)
#     gender = players.get_gender_from_name(name)
#     text = modify_text_with_gender(text, gender)
#
#     return text
