# -*- coding: utf-8 -*-

from nbopen import find_best_server, url_escape, url_path_join
import os.path as op


def get_url(path, profile="default"):
    path = op.expanduser(op.abspath(path))
    server = find_best_server(path, profile)
    if server is None:
        return None
    nbdir = server["notebook_dir"]
    p = op.relpath(path, start=nbdir)
    return url_path_join(server["url"], "notebooks", url_escape(p))
