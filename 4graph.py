import csv

verbs = {}  # глагол:(ipm, r, d, doc, dicts)

with open('freqrnc2011.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[1] == 'v':
            verbs[row[0].replace('ё', 'е')] = tuple(row[2:])

with open('freqs_in_dicts.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[0].replace('ё', 'е') in verbs:
            verbs[row[0].replace('ё', 'е')] += tuple([row[1]])
        else:
            verbs[row[0].replace('ё', 'е')] = tuple(['0', '0', '0', '0', row[1]])

    # print('lemma: ', v, type(v), '\nvalues: ', verbs[v], type(verbs[v]), '\nipm', verbs[v][0], type(verbs[v][0]))

with open('frq_rnc_and_dicts_yo.csv', 'w') as g:
    g.write('lemma\tipm\tr\td\tdoc\tdicts\n')
    for v in verbs:
        if len(verbs[v]) == 4:
            verbs[v] += tuple(['0'])
        g.write(v)
        g.write('\t')
        g.write('\t'.join(verbs[v]))
        g.write('\n')
