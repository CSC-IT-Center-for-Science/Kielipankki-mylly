# TOOL fin-plain-postag.py: "PoS-tag Finnish plaintext" (PoS-tag Finnish plaintext. Produce both the actual output of the underlying tool and a relation where each sentence and token has an explicit identifier.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# OUTPUT output.tsv
# RUNTIME python3

import os, sys
from itertools import groupby
from subprocess import Popen, PIPE

sys.path.append(os.path.join(chipster_module_path, "python"))
sys.path.append(os.path.join(chipster_module_path, "python/xvrt-tools"))
from lib_names2 import base, name

# temporary copy of outsidelib from vrt-tools, primarily to access a
# workable locale, secondarily to use more convenient path machinery
from outsidelib import prebins, prelibs, HFSTBIN, HFSTLIB, utf8ish

name('output.txt', '{}-pos'.format(base('input.txt', '*.txt')),
     ext = 'txt')

name('output.tsv', '{}-pos'.format(base('input.txt', '*.txt')),
     ext = 'rel.tsv')

# finnish-postag in Taito runs its own components with direct paths
# but depends on having hsft-lookup on PATH - remains to be seen
# whether it can run without LD_LIBRARY_PATH in Mylly - readelf -d
# indicates dependence of hfst-lookup on libhfst.so - something does
# go wrong but the symptom in Mylly is "success" with empty output
# files, no message - now *try* with libhfst.so on LD_LIBRARY_PATH -
# does not seem to help - also, finnish-postag also depends on
# hfst-tokenize, which probably also needs libhfst.so, but if that is
# not the problem, what is? Adding HFST to PATH does not help, still
# getting empty output with success status - try invoking the script
# with some error-trapping options.

TOOLBIN = '/appl/ling/finnish-tagtools/1.3.2/bin'
TOOL = ['/bin/bash', '-e', '-E', '-o', 'pipefail',
        os.path.join(TOOLBIN, 'finnish-postag')]

print('does PATH contain hfst bin directory?')
for component in os.environ.get('PATH', '').split(os.pathsep):
    print(component)

def end(*ps):
    for p in ps:
        try:
            # there should be no more
            # stdout nor stderr there
            p.communicate(timeout = 3)
        except TimeoutExpired as exn:
            # things are already bad
            p.kill()
            p.communicate()
    cs = [p.returncode for p in ps]
    if any((c or (c is None)) for c in cs):
        raise Exception('Non-0 return code in: ' + ' '.join(map(str, cs)))

try:
    with Popen(TOOL,
               env = dict(os.environ,
                          LC_ALL = utf8ish(),
                          PATH = prebins(HFSTBIN),
                          LD_LIBRARY_PATH = prelibs(HFSTLIB)),
               stdin = open('input.txt', mode = 'rb'),
               stdout = PIPE) as tokenize:
        # stderr = open('error1.log', mode = 'wb')) as tokenize:
        with Popen(['tee', 'output.txt'],
                   stdin = tokenize.stdout,
                   stdout = PIPE) as tee:
            # stderr = open('error2.log', mode = 'wb')) as tee:
            
            # tee saves the actual output in output.txt; then the
            # following writes a corresponding relation in output.tsv
            
            with open('output.tsv', mode = 'w', encoding = 'UTF-8') as out:
                print('sentok', 'kMsen', 'kMtok', 'word', 'lemma', 'msd',
                      sep = '\t',
                      file = out)
                for k, g in enumerate(( group
                                        for kind, group
                                        in groupby(tee.stdout, bytes.isspace)
                                        if not kind ),
                                      start = 1):
                    for t, w in enumerate(g, start = 1):
                        print('{:04}-{:03}'.format(k, t), k, t, w.decode('UTF-8'),
                              sep = '\t',
                              end = '',
                              file = out)
                # waits with time
                end(tokenize, tee)
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(ev, file = sys.stderr)
    exit(1)
