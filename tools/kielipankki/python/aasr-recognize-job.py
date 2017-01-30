# TOOL aasr-recognize-job.py: "Aalto ASR Recognize Job" (Run a wrapped speech recognition job in the batch system. Use Aalto ASR Recognize Wrap to wrap an audio file.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL script.txt
# OUTPUT OPTIONAL script.textgrid
# OUTPUT OPTIONAL script.eaf
# OUTPUT OPTIONAL error.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# RUNTIME python3

# Made batch stdout and stderr available in Mylly at least for the
# time being. Need to work out the details.

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wrap as lib

lib.process_wrap("Aalto ASR Recognize Wrap",
                 "./script.txt",
                 "./script.textgrid",
                 "./script.eaf",
                 "./stdout.log",
                 "./stderr.log")

# What's with the ./ in the result file names? Those are the be
# brought over to ./ from the work directory in the end.