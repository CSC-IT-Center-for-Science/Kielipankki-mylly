# TOOL kwic-as-tsv.py: "KWIC as TSV"
# (Korp JSON-form concordance as two TSV files, tokens with their annotations in one and structural annotations in the other. Both files contain a sentence counter attribute so that they can be easily joined into one.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT tokens.tsv
# OUTPUT meta.tsv
# RUNTIME python3

import json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('tokens.tsv', names.replace('kwic.json', '-tokens.tsv'))
names.output('meta.tsv', names.replace('kwic.json', '-meta.tsv'))

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# lead sentence/token determines which attributes,

head = list(kwic[0]['tokens'][0]) # lead token
# also: _match (0/1), _sen (counter, also in meta), _tok (counter within _sen)

with open('tokens.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('_match', '_sen', '_tok', *head, sep = '\t', file = out)
    for j, hit in enumerate(kwic):
        for k, token in enumerate(hit['tokens']):
            m = hit['match']
            print(int(m['start'] <= k < m['end']),
                  j, k,
                  *(token[key] for key in head),
                  sep = '\t', file = out)
        
os.rename('tokens.tmp', 'tokens.tsv')

meta = list(kwic[0]['structs'])
# also: _sen (counter, also in head), _start, _end, _corpus

with open('meta.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('_sen', '_start', '_end', '_corpus', *meta, sep = '\t', file = out)
    for j, hit in enumerate(kwic):
        m, c, data = hit['match'], hit['corpus'], hit['structs']
        print(j, m['start'], m['end'], c, *(data[key] for key in meta),
              sep = '\t', file = out)

os.rename('meta.tmp', 'meta.tsv')