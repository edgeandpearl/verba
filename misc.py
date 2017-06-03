# miscellaneous useful stuff

import urllib.request as u_request
import urllib.parse as u_parse
import re
import codecs
import pymysql


def not_there():
    f = codecs.open('i_chosenfordict.csv').read()
    f = f.strip().split('\n')
    regex = re.compile('<tr><td colspan="6">(.*?)</tbody></table>', flags=re.DOTALL)

    for line in f[1:]:
        url = 'http://marker.framebank.ru/verbs_cx.php?lex=' + u_parse.quote(line.split(';')[1])
        page = u_request.urlopen(url).read().decode('utf-8-sig')
        clc_raw = re.findall(regex, page)
        if not clc_raw:
            print(line.split(';')[1], ' not found')
    return


def notfounds():
    nf = """болеть
выращивать
заболеть
заканчивать
закончить
заставлять
изменять
мешать
наступать
оканчивать
окончить
отнести
относить
подождать
соревноваться
фотографировать
вестись
взглянуть
видеться
возрастать
восприниматься
выдаваться
выстроить
выясниться
выясняться
даваться
диктовать
довестись
дожить
завершать
завершиться
задумать
заинтересовать
заканчиваться
закончиться
закрываться
заработать
заставить
затянуться
здравствовать
избавиться
изготовить
изменить
именовать
исчерпать
наблюдаться
накопиться
нарастать
наступить
нацелить
оберегать
обнаружиться
обсуждаться
определиться
определяться
организовывать
осознавать
осознать
отвлекать
отобрать
отпасть
отработать
отыскать
передаваться
писаться
повториться
повторяться
поехать
покрываться
полагать
помешать
поражать
поразить
потребоваться
почитать
пояснить
превышать
прикрыть
присоединиться
присоединяться
приспособить
проводиться
продаваться
продвигаться
продиктовать
продлить
продумать
проработать
протекать
развиваться
разместить
распространяться
расширяться
реагировать
сбыться
свидетельствовать
сказаться
сниматься
совершаться
совпадать
совпасть
содержаться
справиться
сработать
стать
требоваться
увеличиваться
уверить
удалить
украсить
уменьшаться
уменьшиться
упустить
усиливаться
утратить
хватать
хватить
храниться"""
    nf = nf.split('\n')
    regex = re.compile('<tr><td colspan="6">(.*?)</tbody></table>', flags=re.DOTALL)
    losts = []
    multiples = {}
    for verb in nf:
        count = 1
        while True:
            url = u'http://marker.framebank.ru/verbs_cx.php?lex=' + u_parse.quote(verb) + str(count)
            page = u_request.urlopen(url).read().decode('utf-8-sig')
            clc_raw = re.findall(regex, page)
            if clc_raw:
                count += 1
                multiples[verb] = count
            else:
                if count == 1:
                    losts.append(verb)
                break
    with codecs.open('multiples.txt', 'w') as f:
        for verb in multiples:
            f.write(verb + ' ' + str(multiples[verb]))
            f.write('\n')
    with codecs.open('losts.txt', 'w') as f:
        losts = list(set(losts))
        for verb in losts:
            f.write(verb)
            f.write('\n')
    return


def filter_csv():
    with codecs.open('losts.txt', 'r') as f:
        lostverbs = f.read().strip().split('\n')
    with codecs.open('i_chosenfordict.csv', 'r') as f:
        lines = f.read().strip().split('\n')
    with codecs.open('verbs_filtered.csv', 'w') as f:
        for line in lines:
            lemma = line.split(';')[0]
            if lemma not in lostverbs:
                f.write(line)
                f.write('\n')
            else:
                print(lemma, ' is lost!')
    return


def filter_frep():
    tags = []
    with codecs.open('formal_representations.txt') as f:
        chunks = f.read().strip().split(' ')
        for chunk in chunks:
            chunk = re.sub('[^a-zA-Z]', '', chunk)
            tags.append(chunk)
    tags = list(set(tags))
    return tags


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='kSrNt9',
                             db='verba',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


def get_restrictions():
    restrs = []
    for i in range(48658):
        print(i)
        sql = 'SELECT sem_restr FROM arguments WHERE id_colloc="%s"' % str(i+1)
        cursor.execute(sql)
        sem_restr = cursor.fetchall()
        for d in sem_restr:
            restrs.append(d['sem_restr'])
    restrs = list(set(restrs))
    with codecs.open('restrictions.txt', 'w') as f:
        for line in restrs:
            f.write(line)
            f.write('\n')
    return

trans_sem_restr = {}
with codecs.open('restrictions_en.txt', 'r') as f:
    lines = f.read().strip().split('\n')
    for line in lines:
        print(line.split('\t'))
        ru = line.split('\t')[0]
        trans_sem_restr[ru] = trans_sem_restr[line.split('\t')[1]]