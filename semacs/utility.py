# -*- coding: utf-8 -*-

import re
import os
import time


def detect_sequence(names):
    """
    Extract sequences from a list of strings

    >>> detect_sequence(["b1.txt", "a", "a0.txt", "b", "a1.txt", "b0.txt", "c"])
    (['a', 'c', 'b'], {'b[0-9]+.txt': ['b1.txt', 'b0.txt'], 'a[0-9]+.txt': ['a0.txt', 'a1.txt']})

    """
    col = {}
    for name in names:
        pat = re.sub("[0-9]+", "[0-9]+", name)
        if pat not in col:
            col[pat] = []
        col[pat].append(name)
    non_seq = []
    seq = {}
    for pat, ns in col.items():
        if len(ns) == 1:
            non_seq.append(ns[0])
            continue
        seq[pat] = ns
    return non_seq, seq


def get_mtime(path, format_str="%Y/%m/%d-%H:%M:%S"):
    mt = os.stat(path).st_mtime
    return time.strftime(format_str, time.localtime(mt))
