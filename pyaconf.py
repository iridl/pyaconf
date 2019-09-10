import sys
import pyaconf

src = sys.argv[1]
typ = sys.argv[2]

c = pyaconf.load(src)
pyaconf.dump(c, sys.stdout, typ)
