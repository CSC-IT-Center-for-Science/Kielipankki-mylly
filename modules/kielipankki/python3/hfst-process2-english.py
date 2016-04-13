# TOOL hfst-process2-english.py: "HFST Process2 English" (An alternative processor that tokenizes text using an English morphological analyser. Output format depends on the underlying combination of lookup tool, its options, and lexical transducer.)
# INPUT text.txt TYPE GENERIC
# OUTPUT segments.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v383: "3.8.3", v390: "3.9.0"] DEFAULT v383 (HFST Version)
# PARAMETER LineInput TYPE boolean DEFAULT False (Whether each line is an input unit. Default separator is an empty line.)
# PARAMETER PrintAll TYPE boolean DEFAULT False (Whether to print nonmatching text, whatever that is. Default not.)
# PARAMETER PrintWeights TYPE boolean DEFAULT False (Whether to print weights. Default not.)
# PARAMETER OutputFormat TYPE [xerox: "Xerox format", cg: "Constraint Grammar format", segment: "Segment (tokenize)", finnpos: "FinnPos output"] DEFAULT segment (Output format)

# Own library in .../common/python3 should be found on sys.path.

import os
from library.pipeline import hfst_process
from library.errorlog import consolidate

def process_3_8_3():
    home = "/homeappl/appl_taito/ling/hfst/3.8.3"
    processor  = os.path.join(home, "bin", "hfst-proc2")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    of = dict(xerox = '--xerox',
              cg = '--cg',
              segment = '--segment',
              finnpos = '--finnpos')[OutputFormat]

    command = [processor, of]
    if LineInput: command.append('--newline')
    if PrintAll: command.append('--print-all')
    command.append(transducer)

    hfst_process(*command)

def process_3_9_0(of):
    home = "/homeappl/appl_taito/ling/hfst/3.9.0"
    processor  = os.path.join(home, "bin", "hfst-proc2")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    of = dict(xerox = '--xerox',
              cg = '--cg',
              segment = '--segment',
              finnpos = '--finnpos')[OutputFormat]

    command = [processor, of]
    if LineInput: command.append('--newline')
    if PrintAll: command.append('--print-all')
    command.append(transducer)

    hfst_process(*command)

dict(v383 = process_3_8_3, v390 = process_3_9_0)[Version]()

consolidate()