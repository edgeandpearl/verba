# жизнь меняется, и этот скрипт не нужен. пусть останется для истории

import sqlite3
import csv
import urllib.request as u_request
import urllib.parse as u_parse

import codecs
import re

verbs = []


def make_verb_table():  # делаем таблицу из частотного словаря (только глаголы)
    con = sqlite3.connect('testdb.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE verbs (
    id_verb INTEGER PRIMARY KEY AUTOINCREMENT,
    lemma VARCHAR(100),
    freq INTEGER,
    r INTEGER,
    d INTEGER,
    doc INTEGER)''')
    con.commit()

    with open('freqrnc2011.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row[1] == 'v':
                verbs.append(row[0])
                cur.execute('INSERT INTO verbs (lemma, freq, r, d, doc) VALUES ("{lem}", {freq}, {r}, {d}, {doc})'.
                            format(lem=row[0], freq=row[2], r=row[3], d=row[4], doc=row[5]))
                con.commit()
    con.close()
    return


def retrieve_collocations(verb):
    url = u'http://marker.framebank.ru/verbs_cx.php?lex=' + u_parse.quote(verb)
    collocs = {}  # fb-представление:(пример1, [примеры 2-∞])
    regex = re.compile('<tr><td colspan="6">(.*?)</tbody></table>', flags=re.DOTALL)
    page = u_request.urlopen(url).read().decode('utf-8-sig')
    clc_raw = re.findall(regex, page)
    for c in clc_raw:
        main_example = re.findall('_(.*?)&', c)[0]
        represent = re.findall('&nbsp;&nbsp;&nbsp;(.+?)&nbsp;&nbsp', c)[0]
        other_examples = re.findall('&nbsp;<i>(.*?)</i>', c)[0]
        collocs[represent] = (main_example, other_examples)
    return collocs


def make_colloc_table():  # делаем таблицу с коллокациями
    con = sqlite3.connect('testdb.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE collocations (
    id_colloc INTEGER PRIMARY KEY AUTOINCREMENT,
    view VARCHAR(100),
    ex_rus VARCHAR(500),
    ex_rus_par VARCHAR(100),
    ex_eng_par VARCHAR(500),
    id_verb INTEGER, FOREIGN KEY (id_verb) REFERENCES verbs(id_verb))''')
    con.commit()
    return

if __name__ == '__main__':
    make_verb_table()
    noinfo = []
    for verb in verbs:
        d = retrieve_collocations(verb)
        if not d:
            print('NO INFO FOR ', verb)
            noinfo.append(verb)
        else:
            pass
            #for i in d:
                #print(i, '-----', d[i])
        #print('\n\n')
    f = codecs.open('noinfo.txt', 'w')
    for verb in noinfo:
        f.write(verb)
        f.write('\n')
    f.close()
