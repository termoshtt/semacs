# -*- coding: utf-8 -*-

import os.path as op
from functools import wraps
from inspect import getargspec
from logging import getLogger, NullHandler
from .exception import SemacsError

logger = getLogger(__name__)
logger.addHandler(NullHandler())

node_actions = {}
graph_actions = {}


class NodeActionImplError(SemacsError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "NodeAction {} does not return node".format(self.name)


def _wrap(filter_func):
    def decorator(func):
        @wraps(func)
        def wrapper(G, *args, **kwds):
            for node in G.node:
                if not filter_func(node):
                    continue
                try:
                    new_node = func(node, *args, **kwds)
                    if not isinstance(new_node, dict):
                        raise NodeActionImplError(func.__name__)
                    if new_node != node:  # new instance is generated
                        node.clear()
                        node.update(new_node)
                except SemacsError as e:
                    logger.info(str(e))
                    continue
            return G
        spec = getargspec(func)
        nkeys = len(spec.defaults)
        node_actions[func.__name__] = {
            "func": func,
            "args": spec.args[1:-nkeys],
            "kwds": spec.args[nkeys:],
        }
        return wrapper
    return decorator


def type(typename):
    return _wrap(lambda n: n["type"] == typename)


exsits = _wrap(lambda n: op.exists(n["path"]))
file = _wrap(lambda n: op.exists(n["path"]) and op.isfile(n["path"]))
directory = _wrap(lambda n: op.exists(n["path"]) and op.isdir(n["path"]))
all = _wrap(lambda _: True)
