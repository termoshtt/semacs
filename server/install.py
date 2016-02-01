#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import os.path as op
import requests
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from functools import wraps
from contextlib import contextmanager

chunk_size = 1024 * 1024
install_list = []


def add_install(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        sys.stdout.write("Downloading {}...".format(f.__name__))
        sys.stdout.flush()
        res = f(*args, **kwds)
        print("Done")
        return res
    install_list.append(wrapper)
    return wrapper


def download(url, filename, **cfg):
    r = requests.get(url, **cfg)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            f.write(chunk)


@contextmanager
def downloaded_zip(url, **cfg):
    r = requests.get(url, **cfg)
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        zipname = f.name
        for chunk in r.iter_content(chunk_size):
            f.write(chunk)
    with ZipFile(zipname, 'r') as zf:
        yield zf


@add_install
def jquery(jspath, csspath, fontspath):
    fn = "jquery-1.10.2.js"
    url = "http://code.jquery.com/" + fn
    download(url, op.join(jspath, fn))


@add_install
def jquery_cookie(jspath, csspath, fontspath):
    fn = "jquery.cookie.js"
    url = "https://raw.github.com/carhartl/jquery-cookie/master/src/" + fn
    download(url, op.join(jspath, fn))


@add_install
def jquery_blockUI(jspath, csspath, fontspath):
    fn = "jquery.blockUI.js"
    url = "http://malsup.github.io/" + fn
    download(url, op.join(jspath, fn))


@add_install
def jquery_datatables(jspath, csspath, imagepath):
    version = "1.10.4"
    topdir = "DataTables-{}".format(version)
    url = "http://datatables.net/releases/{}.zip".format(topdir)

    with downloaded_zip(url, headers={'User-Agent': "Magic Browser"}) as zf:
        _copy_file(jspath, zf,
                   topdir + "/media/js/jquery.dataTables.min.js")
        _copy_file(csspath, zf,
                   topdir + "/media/css/jquery.dataTables.min.css")
        for name in zf.namelist():
            if not name.find("media/images") is -1 and not name.endswith("/"):
                _copy_file(imagepath, zf, name)

        _copy_file(jspath, zf,
                   topdir + "/extensions/ColReorder/js/dataTables.colReorder.min.js")
        _copy_file(csspath, zf,
                   topdir + "/extensions/ColReorder/css/dataTables.colReorder.min.css")
        _copy_file(imagepath, zf,
                   topdir + "/extensions/ColReorder/images/insert.png")

        _copy_file(jspath, zf,
                   topdir + "/extensions/FixedColumns/js/dataTables.fixedColumns.min.js")
        _copy_file(csspath, zf,
                   topdir + "/extensions/FixedColumns/css/dataTables.fixedColumns.min.css")


@add_install
def bootstrap(jspath, csspath, fontspath):
    url = "https://github.com/twbs/bootstrap/releases/download/v3.3.1/bootstrap-3.3.1-dist.zip"
    with downloaded_zip(url) as zf:
        _copy_file(jspath, zf, "dist/js/bootstrap.min.js")
        _copy_file(csspath, zf, "dist/css/bootstrap.min.css")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.eot")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.svg")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.ttf")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.woff")


@add_install
def multifilter(jspath, csspath, fontspath):
    fn = "multifilter.min.js"
    url = "https://raw.githubusercontent.com/tommyp/multifilter/master/" + fn
    download(url, op.join(jspath, fn))


def _copy_file(path, zf, fn):
    with zf.open(fn) as f_from:
        with open(op.join(path, op.basename(fn)), 'wb') as f_to:
            f_to.write(f_from.read())

if __name__ == '__main__':
    root_dir = op.join(op.dirname(__file__), "static")
    jspath = op.join(root_dir, "js")
    csspath = op.join(root_dir, "css")
    imagepath = op.join(root_dir, "images")
    fontspath = op.join(root_dir, "fonts")
    for path in [root_dir, jspath, csspath, imagepath, fontspath]:
        if not op.exists(path):
            os.mkdir(path)
    for installer in install_list:
        installer(jspath, csspath, fontspath)
