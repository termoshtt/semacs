# -*- coding: utf-8 -*-

import os.path as op
from functools import wraps
from inspect import getargspec
from logging import getLogger, NullHandler
from .exception import SemacsError
from . import io as sio

logger = getLogger(__name__)
logger.addHandler(NullHandler())

actions = {}


def _get_doc(func):
    if func.__doc__:
        for line in func.__doc__.split("\n"):
            if line:
                return line
    return ""


def graph(func):
    spec = getargspec(func)
    nkeys = len(spec.defaults)
    actions[func.__name__] = {
        "type": "graph",
        "func": func,
        "args": spec.args[1:-nkeys],
        "kwds": spec.args[-nkeys:],
        "doc": _get_doc(func),
    }
    return func


class NodeActionImplError(SemacsError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "NodeAction {} does not return node".format(self.name)


def _wrap(filter_func):
    def decorator(func):
        @wraps(func)
        def wrapper(G, *args, **kwds):
            for path, node in G.nodes_iter(data=True):
                node["path"] = path
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
        actions[func.__name__] = {
            "type": "node",
            "func": wrapper,
            "args": spec.args[1:-nkeys],
            "kwds": spec.args[-nkeys:],
            "doc": _get_doc(func),
        }
        return wrapper
    return decorator


def type(typename):
    return _wrap(lambda n: n["type"] == typename)


exsits = _wrap(lambda n: op.exists(n["path"]))
file = _wrap(lambda n: op.exists(n["path"]) and op.isfile(n["path"]))
directory = _wrap(lambda n: op.exists(n["path"]) and op.isdir(n["path"]))
all = _wrap(lambda _: True)


def execute(info, *args, **kwds):
    G = sio.load()
    info["func"](G, *args, **kwds)
    sio.save(G)
