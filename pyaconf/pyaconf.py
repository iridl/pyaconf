"""Yet another config library that is built around python dict and supports json, yaml
"""
# Copyright (c) 2002-2019 Aware Software, inc. All rights reserved.
# Copyright (c) 2005-2019 ikh software, inc. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#
# pyaconf/pyaconf.py
#
import io
import sys
import collections.abc
import json
import yaml
import itertools
import pathlib
import configparser

LOAD_KEY = '__include__'

def logg(*args, **kwargs):
   print(*args, file=sys.stderr, **kwargs)

# --- load ---

def load(src, fmt='auto', path=None):
   """ loads a dict that may include special keyword '__include__' at multiple levels,
   and resolves these includes and returns a dict without includes. It can also read the input dict from a file
   src -- dict|Mapping, FILE|io.StringIO(s), pathlib.Path|str
   fmt -- 'auto' | 'pyaconf' | 'json' | 'yaml' | 'ini'
   path -- is used only when src doesn't contain path info, it is used for error messages and resolve relative include paths
   """
   if path is not None and not isinstance(path, pathlib.Path):
      path = pathlib.Path(path)

   if isinstance(src, collections.abc.Mapping):
      r = _load_dict(src, path)
   elif isinstance(src, io.IOBase):
      if fmt == 'auto':
         raise Exception(f"pyaconf.load: specify fmt (fmt={fmt}, path={path})")
      r = _load_file(src, fmt, path)
   elif isinstance(src, str):
      r = load(pathlib.Path(src), fmt, path)
   elif isinstance(src, pathlib.Path):
      if fmt == 'auto':
         ext = src.suffix
         if ext in _input_extensions:
            fmt = _input_extensions[ext]
         else:
            raise Exception(f"pyaconf.load: cannot derive fmt from file extension, specify fmt (path={src})")

      if path is not None and not src.is_absolute():
         src = path.parent / src

      with open(src, 'r') as f:
         logg(src)
         r = _load_file(f, fmt, src)
   else:
      raise Exception(f"pyaconf.load: illegal type of src (type={typ}, path={path})")
   return r


_input_extensions = {
   '.yaml': 'yaml',
   '.yml': 'yaml',
   '.json': 'json',
   '.pyaconf': 'pyaconf',
   '.ini': 'ini',
}

_output_extensions = {
   '.yaml': 'yaml',
   '.yml': 'yaml',
   '.json': 'json',
}

def _load(x, path):
   if isinstance(x, collections.abc.Mapping):
      r = _load_dict(x, path)
   elif isinstance(x, list):
      r = _load_list(x, path)
   else:
      r = x
   return r

def _load_dict(x, path):
   rs = []
   if LOAD_KEY in x:
      loads = x[LOAD_KEY]
      for v in (loads if isinstance(loads, list) else [loads]):
         rs.append(load(*v, path=path) if isinstance(v, tuple) else load(v, path=path))
   y = {}
   for k,v in x.items():
      if k != LOAD_KEY:
         y[k] = _load(v, path)
   rs.append(y)
   r = merge(rs) if len(rs) > 1 else rs[0]
   return r

def _load_list(x, path):
   return [_load(a, path) for a in x]


def _load_file(f, fmt, path):
   if fmt == 'yaml':
      x = yaml.load(f, Loader=yaml.Loader)
   elif fmt == 'json':
      x = json.load(f)
   elif fmt == 'pyaconf':
      c = f.read()
      genv = {}
      exec(compile(c, path, 'exec'), genv)
      x = eval('config()', genv)
   elif fmt == 'ini':
      x = _load_ini(f, path)
   else:
      raise Exception(f"pyaconf.load: fmt is not supported (fmt={fmt}, path={path})")
   return _load(x, path)

def _load_ini(f, path):
   c = configparser.ConfigParser()
   c.read_file(f)
   r = {}
   for s in c.sections():
      if s != 'DEFAULT':
         r[s] = dict(c[s])
   return r


# --- merge ---

def merge(xs):
   """ merges the list of dicts (that dont contain includes) and returns a new dict
   where the values of the first dict are updated recursively by the values of the second dict.
   """
   z = {}
   for x in xs:
      z = _deep_merge(z, x)
   return z

def _deep_merge(z, x):
   if isinstance(z, collections.abc.Mapping) and isinstance(x, collections.abc.Mapping):
      r = _deep_merge_dicts(z, x)
   elif isinstance(z, list) and isinstance(x, list):
      r = _deep_merge_lists(z, x)
   else:
      r = x
   return r

def _deep_merge_dicts(z, x):
   r = {}
   for k,v in z.items():
      if k in x:
         r[k] = _deep_merge(v, x[k])
      else:
         r[k] = v
   for k,v in x.items():
      if k not in r:
         r[k] = v
   return r

def _deep_merge_lists(z, x):
   return [_deep_merge(a,b) for (a,b) in (itertools.zip_longest(z,x) if len(x) > len(z) else zip(z,x))]
      

# --- dump ---

def dump(x, dst=sys.stdout, fmt='auto'):
   """ Dumps resolved (without includes) config in json or yaml format. It doesn't preserve comments either. 
   """
   if isinstance(dst, io.IOBase):
      if fmt == 'auto':
         raise Exception(f"pyaconf.dump: specify fmt (fmt={fmt})")
      r = _dump_file(x, dst, fmt)
   elif isinstance(dst, str):
      r = dump(x, pathlib.Path(dst), fmt)
   elif isinstance(dst, pathlib.Path):
      if fmt == 'auto':
         ext = dst.suffix
         if ext in _output_extensions:
            fmt = _output_extensions[ext]
         else:
            raise Exception(f"pyaconf.dump: cannot derive fmt from file extension, specify fmt (path={dst})")
      with open(dst, 'w') as f:
         r = _dump_file(x, f, fmt)
   else:
      raise Exception(f"pyaconf.dump: illegal type of dst")

def _dump_file(x, f, fmt):
   if fmt == 'json':
      json.dump(x, f, sort_keys=True, indent=3)
   elif fmt == 'yaml':
      yaml.dump(x, f, default_style='', default_flow_style=False)
   else:
      raise Exception(f"pyaconf.dump: illegal fmt (fmt={fmt})")
   

