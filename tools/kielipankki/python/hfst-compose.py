# TOOL hfst-compose.py: "Compose transducers"
# (Compose HFST transducers. The second input archive can contain as many transducers as the first, or one transducer.)
# INPUT input1.hfst TYPE GENERIC
# INPUT input2.hfst TYPE GENERIC
# OUTPUT output.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('output.hfst', names.replace('input1.hfst', '-o.hfst'))

hfst.setenv(Version)

with Popen(['hfst-compose', '-o', 'output.hfst',
            'input1.hfst',
            'input2.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-compose' if VersionLog == 'produce' else None)
