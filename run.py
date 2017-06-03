from flask import Flask, render_template, Response, redirect, url_for, request
import pymysql
from search_rnc import *
import random
import codecs

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='kSrNt9',
                             db='verba',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

with codecs.open('./db/verbs.csv', 'r') as f:
    lines = f.read().strip().split('\n')
    verbs = [line.split(';')[1] for line in lines[1:]]

trans_sem_restr = {}
with codecs.open('restrictions_en.txt', 'r') as f:
    lines = f.read().strip().split('\n')
    for line in lines:
        trans_sem_restr[line.split('\t')[0]] = line.split('\t')[1]


@app.route('/')
def index():
    placeholder = random.choice(verbs)
    if not request.args:
        return render_template('main.html', message=None, placeholder=placeholder)
    elif request.args['q'] == '':
        return render_template('main.html', message='Задан пустой поисковой запрос.', placeholder=placeholder)
    else:
        try:
            lemma = request.args['q']
            sql = 'SELECT * FROM verbs WHERE lemma="%s"' % lemma
            cursor.execute(sql)
            id_verb = cursor.fetchone()['id_verb']
            sql = 'SELECT * FROM collocations WHERE id_verb="%s"' % id_verb
            cursor.execute(sql)
            collocations = cursor.fetchall()
            arguments = []
            for collocation in collocations:
                sql = 'SELECT form_repr, oblig, sem_restr FROM arguments WHERE id_colloc="%s"' % collocation['id_col']
                cursor.execute(sql)
                arguments.append(cursor.fetchall())
            le = len(collocations)
            return render_template('article.html', lemma=lemma, collocations=collocations, id_verb=id_verb, le=le,
                                   lang='ru', arguments=arguments, len_arguments=len(arguments))
        except TypeError:
            return render_template('main.html', message='Коллокации для слова %s не найдены' % request.args['q'])


@app.route('/ru')
def ru():
    return redirect('/')


@app.route('/en')
def en():
    placeholder = random.choice(verbs)
    if not request.args:
        return render_template('main_EN.html', message=None, placeholder=placeholder)
    elif request.args['q'] == '':
        return render_template('main_EN.html', message='The search query is empty.', placeholder=placeholder)
    else:
        try:
            lemma = request.args['q']
            sql = 'SELECT * FROM verbs WHERE lemma="%s"' % lemma
            cursor.execute(sql)
            id_verb = cursor.fetchone()['id_verb']
            sql = 'SELECT * FROM collocations WHERE id_verb="%s"' % id_verb
            cursor.execute(sql)
            collocations = cursor.fetchall()
            arguments = []
            for collocation in collocations:
                sql = 'SELECT form_repr, oblig, sem_restr FROM arguments WHERE id_colloc="%s"' % collocation['id_col']
                cursor.execute(sql)
                arguments.append(cursor.fetchall())
            le = len(collocations)
            return render_template('article.html', lemma=lemma, collocations=collocations, id_verb=id_verb, le=le,
                                   lang='en', arguments=arguments, len_arguments=len(arguments),
                                   trans_sem_restr=trans_sem_restr)
        except TypeError:
            return render_template('main.html', message='No collocations found for %s' % request.args['q'])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/about_en')
def about_en():
    return render_template('about_EN.html')


@app.route('/examples')
def examples():
    lang = request.args['lang']
    id_col = request.args['id_col']
    lemma = request.args['lemma']
    sql = 'SELECT * FROM collocations WHERE id_col="%s"' % id_col
    cursor.execute(sql)
    fetchone = cursor.fetchone()
    formal_repr = fetchone['formal_repr']
    title_example = fetchone['title_example']
    para_examples = search_in_rnc(formal_repr, lemma)
    mono_examples = search_in_rnc(formal_repr, lemma, parallel=False)
    return render_template('examples.html', formal_repr=formal_repr, lemma=lemma, para=para_examples, mono=mono_examples,
                           lang=lang, title_example=title_example, id_col=id_col)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/contacts_en')
def contacts_en():
    return render_template('contacts_EN.html')


@app.route('/<anything>')
def anything(anything):
    return render_template('404.html')


app.run(debug=True)
