# -*- coding: utf-8 -*-

from .. import action

@action.all
def do_nothing(node, arg1, key=2, key2=None):
    return node


@action.graph
def do_nothing_graph(G, arg, key1=2):
    pass
