# -*- coding: utf-8 -*-

import os.path as op
import glob
from importlib import import_module


__all__ = [op.basename(f)[:-3]
           for f in glob.glob(op.join(op.dirname(__file__), "*.py"))
           if op.basename(f) != "__init__.py"]

for m in __all__:
    import_module("semacs.actions." + m)
