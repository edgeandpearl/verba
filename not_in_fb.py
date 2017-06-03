import codecs
import urllib.parse as u_parse
import urllib.request as u_request
import re

f = codecs.open('freqrnc2011.csv', 'r')
fd = f.read().strip().split('\n')
verbs = [line.split('\t')[0] for line in fd if line.split('\t')[1] == 'v']
f.close()

g = codecs.open('not_in_fb.txt', 'a')
for v in verbs[4000:]:
    url = u'http://marker.framebank.ru/verbs_cx.php?lex=' + u_parse.quote(v)
    page = u_request.urlopen(url).read().decode('utf-8-sig')
    regex = re.compile('<tr><td colspan="6">(.*?)</tbody></table>', flags=re.DOTALL)
    m = re.search(regex, page)
    if not m:
        print(v)
        g.write(v)
        g.write('\n')
g.close()