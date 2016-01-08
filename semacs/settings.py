# -*- coding: utf-8 -*-


import os.path as op
import yaml
from .exception import SemacsError


preset = {
    "storage": {
        "type": "JSON",
        "filename": op.expanduser("~/.semacs.graph.json"),
    },
}


def load(key=None):
    setting = preset.copy()
    prefix = op.abspath(op.expanduser("~/.semacs"))
    for ext in [".yaml", ".yml"]:
        if not op.exists(prefix + ext):
            continue
        with open(prefix + ext, "r") as f:
            cfg = yaml.load(f)
        try:
            setting.update(cfg)
        except TypeError:
            raise SemacsError("Setting file must be hash.")
    if key:
        return setting[key]
    else:
        return setting
