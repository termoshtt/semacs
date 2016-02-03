# -*- coding: utf-8 -*-

from .. import action
import os.path as op


@action.graph
def check(G):
    for path, info in G.nodes_iter(data=True):
        info["path"] = path
        if info["type"] == "project":
            info["type"] = "tag"
        if "name" not in info or not info["name"]:
            info["name"] = op.basename(path)
