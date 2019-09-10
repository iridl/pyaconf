# pyaconf - layered config library built around python dict

Pyaconf is yet another config library that has the following features:

* Built around python dicts, json and yaml
* All configs are json compatible dicts
* Supports layered configs via `__include__` dict entry, for example:

```yaml
__include__: boo.json
user: romeo
password: romeoalpha
```

* Can output configs in `.json` and `.yaml`
* Supports `.ini` input format as understood by python's `configparser`
* Very simple API: `load`, `dump`, and for more advance use `merge`
* Supports dynamic configs written in Python `.pyaconf`, for example:

```python
import os
def config():
   return dict(
      __include__ = "secret.yml"
      user = "romeo", 
      password = os.environ['PASSWORD']
      database = dict(
         __include__ = "db.ini"
      )
   )
```

* Provides command line utility that resolves includes and python configs and outputs a static config in json or yaml that can be consumed by an application written in any language

## API

* `load` takes in a dict that may include special keyword `__include__` at multiple levels, and it resolves these includes and returns a dict without includes. It can also read the input dict from a file.

```python
load(path: string or pathlib.Path | fp: FILE or io. | conf: dict w/ includes, fmt: string = 'auto' ('auto'|'pyaconf'|'json'|'yaml'|'ini') -> dict w/o includes; if fmt=auto, deduces format by extension (.yaml, .yml, .json., .pyaconf, .ini)
```

* `dump` outputs the resulting (resolved) config in yaml or json.

```python
dump(d1: dict w/o includes, d2: dict w/o includes) -> dict w/o includes -- recursively merges dicts 
```

* `merge` simply merges two dicts (that dont contain includes) and returns a new dict where the values of the first dict are updated recursively by the values of the second dict.

merge(ds) -> list of dicts w/o includes

## Other

* First level of a config must be a dict.
* Reserved key `__include__` if present, should contain a path or list of paths to load. A path can be a string or a binary tuble containing the string and the format.
* Python format has to contain a parameterless function config that returns dict w/o includes

```python
    import os
    import pyaconf
    def config():
       prefix = "/aaa/bbb"
       conf = dict(
          __include__ = [
             "foo.json",
             ("boo.config","yaml"),
             "zoo.pyaconf",
          ],
          prefix = prefix,
          full_prefix = prefix + "/xyz",
          dbpool = pyaconf.merge(
             pyaconf.load(dict(
                __include__ = "zoo.pyaconf",
                database = "geom",
                host = "localhost",
                user = os.environ["DATABASE_USER"],
                password = None,
             )),
             pyaconf.loadf("secrets.yaml")
          )
       )
       return conf
```

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
