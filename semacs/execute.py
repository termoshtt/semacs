# -*- coding: utf-8 -*-

import networkx as nx


def node(func, *args, **kwds):
    n = {}
    func(n, *args, **kwds)


def graph(func, *args, **kwds):
    G = nx.DiGraph()
    func(G, *args, **kwds)


def execute(info, *args, **kwds):
    print(info)
    return {
        "node": node,
        "graph": graph,
    }[info["type"]](info["func"], *args, **kwds)
