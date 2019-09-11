# pyaconf - yet another config library built around python dictionary

Pyaconf is a config library that is built around python dictionary and supports dynamic python, json, yaml, and ini formats with inheritance.
It features:

* All configs are json compatible dicts.
* Supports layered configs (inheritance) via `__include__` dict entry, for example, the following yaml config would read the dictionary defined from config `boo.json` and then will update it with `user` and `password` from this config:

```yaml
__include__: boo.json
user: romeo
password: romeoalpha
```

* Simple API: `load`, `dump`, and for more advanced use `merge`.
* Supports dynamic configs written in Python `.pyaconf`, for example:

```python
import os
def config():
   return dict(
      __include__ = ["secret.yml"],
      user = "romeo", 
      password = os.environ['PASSWORD'],
      database = dict(
         __include__ = "db.ini",
      ),
   )
```

* Allows to output configs in `.json` and `.yaml`. Provides two shell scripts.
* Supports `.ini` input format as understood by python's `configparser`.

## API

### load

```python
def load(src, fmt='auto', path=None):
   """ loads a dict that may include special keyword '__include__' at multiple levels,
   and resolves these includes and returns a dict without includes. It can also read the input dict from a file
   src -- dict|Mapping, FILE|io.StringIO(s), pathlib.Path|str
   fmt -- 'auto' | 'pyaconf' | 'json' | 'yaml' | 'ini'
   path -- is used only when src doesn't contain path info, it is used for error messages and resolve relative include paths
```

### dump

```python
def dump(x, dst=sys.stdout, fmt='auto'):
   """ Dumps resolved (without includes) config in json or yaml format. It doesn't preserve comments either. 
   x -- dict|Mapping
   dst -- FILE|io.StringIO(s), pathlib.Path|str
   fmt -- 'auto' | 'json' | 'yaml'
   """
```


### merge

```python
def merge(xs):
   """ merges the list of dicts (that dont contain includes) and returns a new dict
   where the values of the first dict are updated recursively by the values of the second dict.
   xs -- a list of dicts
   """
```

## Scripts

* pyaconf2json -- loads and merges multiple configs and outputs in json format

* pyaconf2yaml -- loads and merges multiple configs and outputs in yaml format

## License

OSI Approved 3 clause BSD License

## Prerequisites

* Python 3.7+

## Installation

If prerequisites are met, you can install `pyaconf` like any other Python package, using pip to download it from PyPI:

    $ pip install pyaconf

or using `setup.py` if you have downloaded the source package locally:

    $ python setup.py build
    $ sudo python setup.py install
