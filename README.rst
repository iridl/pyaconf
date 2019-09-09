pyaconf - Yet another config library that is built around Python dict
=====================================================================

Pyaconf is built around Python dicts and supports json, yaml, ini and maybe other dict
compatible formats in the future. Supports layered configs (inheritance, overrides). 

* A configuration is a json compatible dict. Yaml and pyaconf formats must be json compatible.
* The library API is very simple, it provides only three functions ``load`` and ``merge``, and ``dump``.
* The first function `load` takes in a dict that may include special keyword '__include__' at multiple levels, and it resolves these includes and returns a dict without includes. It can also read the input dict from a file.

```
load(path: string or pathlib.Path | fp: FILE or io. | conf: dict w/ includes, fmt: string = 'auto' ('auto'|'pyaconf'|'json'|'yaml'|'ini') -> dict w/o includes; if fmt=auto, deduces format by extension (.yaml, .yml, .json., .pyaconf, ini)
```

* The second function ``merge`` simply merges two dicts (that dont contain includes) and returns a new dict where the values of the first dict are updated recursively by the values of the second dict.

```
merge(d1: dict w/o includes, d2: dict w/o includes) -> dict w/o includes -- recursively merges dicts 
```

* The third functions ``dump`` outputs the resulting (resolved) config in yaml or json.

```
dump(d1: dict w/o includes, d2: dict w/o includes) -> dict w/o includes -- recursively merges dicts 
```

* First level of a config must be a dict.
* Reserved key "__include__" if present, should contain a path or list of paths to load. A path can be a string or a binary tuble containing the string and the format.
* Python format has to contain a parameterless function config that returns dict w/o includes

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

License
-------

OSI Approved 3 clause BSD License

Prerequisites
-------------

* Python 3.7+

Installation
------------

If prerequisites are met, you can install `pyaconf` like any other Python package, using pip to download it from PyPI:

    $ pip install pyaconf

or using `setup.py` if you have downloaded the source package locally:

    $ python setup.py build
    $ sudo python setup.py install
