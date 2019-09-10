import sys
import pyaconf

try:
   src = sys.argv[1]
   typ = sys.argv[2]

   c = pyaconf.load(src)
   pyaconf.dump(c, sys.stdout, typ)

except Exception as e:
   print(e, file=sys.stderr)
