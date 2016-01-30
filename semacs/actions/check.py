# -*- coding: utf-8 -*-

from .. import action


@action.graph
def check(G):
    for path, info in G.nodes_iter(data=True):
        info["path"] = path
