# TOOL hfst-strings2fst.py: "Compile strings"
#     (Compiles string pairs into transducers.)
# INPUT stringen.txt TYPE GENERIC
# OUTPUT duceren.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Format
#     TYPE [tropical: "OpenFST Tropical",
#           logarithmic: "OpenFST Log"]
#     DEFAULT tropical
#     (HFST binary format)
# PARAMETER Union
#     TYPE [many: "many transducers",
#           one: "one transducer"]
#     DEFAULT many
#     (How to represent the union of many string pairs)
# PARAMETER InputForm
#     TYPE [strings: "symbol strings",
#           spacedstrings: "spaced symbol strings",
#           symbols: "pair strings",
#           spacedsymbols: "spaced pair strings"]
#     DEFAULT strings
#     (Format of input lines)
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

# To add weight normalization options --norm, --log, --log10.
# To add epsilon.
# To add multichar-symbol file.

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name # TODO
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('duceren.hfst', names.replace('stringen.txt', '.hfst'))

hfst.setenv(Version)

FMT = dict(tropical = 'openfst-tropical',
           logarithmic = 'openfst-log')[Format]

inputform = dict(strings = [],
                 spacedstrings = ['--has-spaces'],
                 symbols = ['--pairstrings'],
                 spacedsymbols = ['--pairstrings', '--has-spaces'])[InputForm]

unionmode = dict(many = [],
                 one = ['--disjunct'])[Union]

with Popen(['hfst-strings2fst', '-o', 'duceren.hfst',
            '--format', FMT]
           + inputform
           + unionmode
           + ['stringen.txt'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'duceren.hfst',
            version = 'hfst-strings2fst' if VersionLog == 'produce' else None)
