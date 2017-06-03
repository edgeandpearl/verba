import codecs
import re

f = codecs.open('./dicts/txt/UNCUT_verbi_italiano_russo.txt', 'r')
v_it = f.read()
f.close()
v_it = re.sub('(\(.*?\))', '', v_it)
v_it = re.sub('[^а-яА-Я\s]+', '', v_it)
v_it = re.sub('й', 'й', v_it)
v_it = re.sub('ё', 'ё', v_it)
v_it = re.sub('\s', ' ', v_it)
v_it = re.sub(' +', '\n', v_it)
g = codecs.open('./dicts/txt/verbi_italiano_russo_FINE.txt', 'w', 'utf-8-sig')
g.write(v_it)
g.close()
