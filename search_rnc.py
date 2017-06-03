from urllib import parse as u_parse
from urllib import request as u_request
import re

POS = {'Noun': 'S', 'Adjective': 'A', 'Adverb': 'ADV', 'Predicate': 'PRAEDIC', 'Prep.': 'PR'}
FEATURES = {'instrumental': 'ins', 'dative': 'dat', 'accusative': 'acc', '(imperative': 'imper',
                'infinitive': 'inf', 'genitive': 'gen', 'locative': 'loc', 'nominative': 'nom', 'passive': 'pass'}


def make_query_as_list(formal_repr, verb):
    query = []  # query for each word as a tuple
    raw_query = formal_repr.split(' ')
    raw_query_no_variation = formal_repr
    query_part = []
    variations = re.findall('{.+?}', formal_repr)
    for variation in variations:
        try:
            var1 = re.findall('{(.+?)/', variation)[0]
        except:
            continue
        raw_query_no_variation = raw_query_no_variation.replace(variation, var1)
    raw_query_no_variation = re.sub('[\(\)]', ' ', raw_query_no_variation)
    raw_query_no_variation = raw_query_no_variation.split(' ')
    for tag in raw_query_no_variation:
        tag = re.sub('^\W*(.*?)\W*$', '\\1', tag)
        if tag in POS:
            query.append(query_part)
            query_part = list()
            query_part.append(POS[tag])
        elif tag in FEATURES:
            query_part.append(FEATURES[tag])
        elif tag == 'Verb':
            query.append(query_part)
            query_part = list()
            query_part.append(verb)
        elif re.match('[а-яА-Я]+', tag):
            query.append(query_part)
            query_part = list()
            query_part.append(tag)
            query.append(query_part)
            query_part = list()
        else:
            pass
    query.append(query_part)
    while [] in query:
        query.remove([])
    return query  # [[characteristics], [for], [each], [word]] in the query

"""
f = codecs.open('./db/collocations.csv')
g = codecs.open('./db/verbs.csv')
lines = f.read().strip().split('\n')[1:]
verbs = g.read().strip().split('\n')[1:]
verb = ''
for line in lines:
    fr = line.split(';')[3]
    id_verb = line.split(';')[-1]
    for row in verbs:
        if row.split(';')[0] == id_verb:
            verb = row.split(';')[1]
            break
    q = make_query(fr, verb)
    print(q)
"""


def make_url_for_request(query_list, parallel=True):
    url_base = 'http://search2.ruscorpora.ru/search.xml'
    if parallel:
        params = {'mysize': '24681277', 'mysentsize': '1608376', "text": "lexgramm", "mode": "para", "sort": "gr_tagging",
                  "env": "alpha", 'mycorp': '(lang:"eng" | lang_trans:"eng")'}
    else:
        params = {"env": "alpha", "text": "lexgramm", "mode": "main", "sort": "gr_tagging", 'lang': 'ru', 'nodia': '1'}
    for i in range(len(query_list)):
        n = i + 1
        params['parent'+str(n)] = 0
        params['level'+str(n)] = 0
        params['sem-mod'+str(n)] = 'sem'
        params['sem-mod'+str(n)] = 'sem2'
        if n > 1:
            params['min'+str(n)] = 1
            params['max'+str(n)] = 1
        if query_list[i][0] not in [POS[key] for key in POS]:
            para = ''.join(('lex', str(n)))
            params[para] = query_list[i][0]
        else:
            para = ''.join(('gramm', str(n)))
            params[para] = u' '.join(query_list[i])
    url_params = u_parse.urlencode(params)
    url = '?'.join((url_base, url_params))
    return url


def get_examples(url, parallel=True):  # url for search request
    page = u_request.urlopen(url).read().decode('windows-1251')
    if parallel:
        regex = re.compile('<table width="100%" cellspacing="10">(.*?<span class="doc">.*?)<span class="doc">',
                           flags=re.DOTALL)
    else:
        regex = re.compile('<table width="100%" cellspacing="10">(.*?)<span class="doc">', flags=re.DOTALL)
    raw_examples = re.findall(regex, page)
    for i in range(len(raw_examples)):
        raw_examples[i] = re.sub('<span class="b-wrd-expl g-em".*?>(.*?)</span>', '(((((\\1)))))', raw_examples[i],
                                 flags=re.DOTALL)
        raw_examples[i] = re.sub('<.*?>', '', raw_examples[i], flags=re.DOTALL)
        raw_examples[i] = re.sub('\[.*?\]', '', raw_examples[i], flags=re.DOTALL)
        # print(len(raw_examples[i]), raw_examples[i])
        raw_examples[i] = re.sub('\(\(\(\(\((.*?)\)\)\)\)\)', '<div class="searched_item">\\1</div>', raw_examples[i],
                                 flags=re.DOTALL)
        if parallel:
            raw_examples[i] = raw_examples[i].split('&#8592;…&#8594;')
    return raw_examples


def search_in_rnc(formal_repr, verb, parallel=True):
    query_list = make_query_as_list(formal_repr, verb)
    url = make_url_for_request(query_list, parallel=parallel)
    examples = get_examples(url, parallel=parallel)
    return examples


if __name__ == '__main__':
    examples = search_in_rnc('Noun (nominative) Verb Noun (accusative)', 'купить')
    for example in examples:
        print(example)
