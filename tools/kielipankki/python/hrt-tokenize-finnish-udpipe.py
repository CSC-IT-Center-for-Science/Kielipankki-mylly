# TOOL hrt-tokenize-finnish-udpipe.py: "Tokenize Finnish HRT with UDPipe" (Tokenize Finnish HRT into VRT with UDPipe.)
# INPUT input.hrt TYPE GENERIC
# OUTPUT output.vrt
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'hrt-tokenize-udpipe')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.hrt', '*.hrt'),
     ext = 'vrt.txt')

try:
    with Popen(['python3', PROG],
               stdin = open('input.hrt', mode = 'rb'),
               stdout = open('output.vrt', mode = 'wb'),
               stderr = open('error.log', mode = 'wb')) as tokenize:
        pass
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(et, ev, tr, sep = '\n', file = sys.stderr)
    exit(1)