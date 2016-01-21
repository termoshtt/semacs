#!/usr/bin/env python
# -*- coding: utf-8 -*-

import semacs
import os.path as op
from flask import Flask, render_template
app = Flask(__name__)


def _fill_name(nodes):
    for t in nodes:
        if "name" not in t or not t["name"]:
            t["name"] = op.basename(t["path"])


@app.route('/')
def home():
    return render_template("layout.html")


@app.route('/runs')
def runs():
    G = semacs.io.load()
    runs = [d for n, d in G.nodes_iter(data=True) if d["type"] == "run"]
    _fill_name(runs)
    return render_template("runs.html", runs=runs)


@app.route("/tags")
def tags():
    G = semacs.io.load()
    tags = [d for n, d in G.nodes_iter(data=True) if d["type"] == "tag"]
    _fill_name(tags)
    return render_template("tags.html", tags=tags)


@app.route("/ipynbs")
def ipynbs():
    return "IPython Notebooks"

if __name__ == '__main__':
    app.debug = True
    app.run()
