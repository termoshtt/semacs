# -*- coding: utf-8 -*-

import os.path as op
import json
from contextlib import contextmanager
from networkx.readwrite import json_graph
import fasteners

from . import settings
from .exception import SemacsError


def _validate_settings(cfg):
    if "type" not in cfg:
        raise SemacsError("storage type is not specified")
    if cfg["type"].upper() != "JSON":
        raise SemacsError("storage must be JSON in this version")
    if "filename" not in cfg:
        raise SemacsError("Filename is not specified")
    cfg["filename"] = op.expanduser(cfg["filename"])
    if not op.exists(cfg["filename"]):
        raise SemacsError("JSON File does not found")


def load():
    cfg = settings.load("storage")
    _validate_settings(cfg)
    with open(cfg["filename"], "r") as f:
        d = json.load(f)
    return json_graph.node_link_graph(d)


def save(G):
    d = json_graph.node_link_data(G)
    cfg = settings.load("storage")
    _validate_settings(cfg)
    with open(cfg["filename"], "w") as f:
        json.dump(d, f)


@contextmanager
def graph():
    with fasteners.InterProcessLock("/tmp/semacs/load_main_json"):
        G = load()
        yield G
        save(G)
