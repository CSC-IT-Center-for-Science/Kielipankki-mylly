# TOOL tsv-sample.py: "Random part (aka subset) of a relation"
# (Makes a random sample of the elements of a relation, aka a set of records.)
# INPUT one.tsv TYPE GENERIC
# OUTPUT sample.tsv
# PARAMETER size TYPE INTEGER FROM 0 DEFAULT 20
# RUNTIME python3

# This is not technically an operation of the relation algebra but
# this is technically an action of a random source on the algebra.
# Something rather like that anyway.

import os, random, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('one.tsv', '.tsv')
names.output('sample.tsv', names.replace('one.tsv', '-samp.tsv'))

with open('one.tsv', encoding = 'utf-8') as fin:
    head = next(fin1).rstrip('\n').split('\t')
    population = list(tuple(line.rstrip('\n').split('\t')) for line in fin1)
    
    if len(population) < size:
        print('Sample of {} is larger than population of {}'
              .format(size, len(population)),
              file = sys.stderr)
        exit(1)
        
    sample = random.sample(population, size)

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*head, sep = '\t', file = out)
    for record in sample:
        print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'sample.tsv')
