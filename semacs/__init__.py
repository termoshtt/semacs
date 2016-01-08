# -*- coding: utf-8 -*-

from importlib import import_module

all = ["io", "settings", "exception"]

for m in all:
    import_module("semacs." + m)
