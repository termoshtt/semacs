# -*- coding: utf-8 -*-

from .. import action


@action.all
def do_nothing(node, arg1, key=2, key2=None):
    print("node", node)
    print("arg1", arg1)
    print("key", key)
    print("key2", key2)
    return node


@action.graph
def do_nothing_graph(G, arg, key1=2):
    """ Do nothing! for Graph

    some other strings...
    """
    print("Graph", G)
    print("arg", arg)
    print("key1", key1)
