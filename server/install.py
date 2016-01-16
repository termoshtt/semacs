#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import os.path as op
import urllib2
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from functools import wraps


def show_progress(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            sys.stdout.write("Downloading {}...".format(name))
            sys.stdout.flush()
            res = f(*args, **kwds)
            print("Done")
            return res
        return wrapper
    return decorator


@show_progress("jQuery")
def install_jquery(jspath):
    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    with open(op.join(jspath, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())


@show_progress("jQuery Cookie")
def install_jquery_cookie(jspath):
    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/src/"\
        + jquery_cookie_filename
    with open(op.join(jspath, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())


@show_progress("jQuery blockUI")
def install_jquery_blockUI(jspath):
    jquery_blockUI_filename = "jquery.blockUI.js"
    jquery_blockUI_url = "http://malsup.github.io/" + jquery_blockUI_filename
    with open(op.join(jspath, jquery_blockUI_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_blockUI_url).read())


@show_progress("jQuery datatables")
def install_jquery_datatables(jspath, csspath, imagepath):
    version = "1.10.4"
    topdir = "DataTables-{}".format(version)
    url = "http://datatables.net/releases/{}.zip".format(topdir)

    req = urllib2.Request(url,
                          headers={'User-Agent': "Magic Browser"})
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        zipname = f.name
        f.write(urllib2.urlopen(req).read())

    with ZipFile(zipname, 'r') as zf:
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


@show_progress("Bootstrap")
def install_bootstrap(jspath, csspath, fontspath):
    bootstrap_version = "3.3.1"
    bootstrap_url = "https://github.com/twbs/bootstrap/releases/download/"\
        + "v{version}/bootstrap-{version}-dist.zip"\
        .format(version=bootstrap_version)
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        bootstrap_name = f.name
        f.write(urllib2.urlopen(bootstrap_url).read())

    with ZipFile(bootstrap_name, 'r') as zf:
        _copy_file(jspath, zf, "dist/js/bootstrap.min.js")
        _copy_file(csspath, zf, "dist/css/bootstrap.min.css")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.eot")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.svg")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.ttf")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.woff")


@show_progress("multifilter")
def install_multifilter(jspath):
    filename = "multifilter.min.js"
    url = "https://raw.githubusercontent.com/tommyp/multifilter/master/" \
        + filename
    with open(op.join(jspath, filename), "w") as f:
        f.write(urllib2.urlopen(url).read())


def _copy_file(path, zf, fn):
    with zf.open(fn) as f_from:
        with open(op.join(path, op.basename(fn)), 'w') as f_to:
            f_to.write(f_from.read())

if __name__ == '__main__':
    ROOT = op.dirname(__file__)
    jspath = op.join(ROOT, "static/js")
    csspath = op.join(ROOT, "static/css")
    imagepath = op.join(ROOT, "static/images")
    fontspath = op.join(ROOT, "static/fonts")
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)
    if not os.path.exists(fontspath):
        os.mkdir(fontspath)

    install_jquery(jspath)
    install_jquery_cookie(jspath)
    install_jquery_blockUI(jspath)
    install_jquery_datatables(jspath, csspath, imagepath)
    install_bootstrap(jspath, csspath, fontspath)
    install_multifilter(jspath)
