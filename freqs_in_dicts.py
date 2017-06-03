import codecs
import os

freqd = {}

for root, dirs, files in os.walk('./dicts/txt'):
    for file in files:
        if not file.startswith('UNCUT') and not file.startswith('.'):
            print(file)
            f = codecs.open('./dicts/txt/' + file, 'r', 'utf-8')
            text = f.read().lower()
            words = set([line for line in text.strip().split()])
            for word in words:
                if word not in freqd:
                    freqd[word] = 0
                freqd[word] += 1
            f.close()

print(len(freqd))

g = codecs.open('freqs_in_dicts.csv', 'w')
for word in freqd:
    g.write(word)
    g.write('\t')
    g.write(str(freqd[word]))
    g.write('\n')
g.close()
