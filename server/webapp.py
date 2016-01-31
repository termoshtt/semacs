#!/usr/bin/env python
# -*- coding: utf-8 -*-

import semacs
import os
import os.path as op
from flask import Flask, render_template, jsonify, redirect
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("layout.html")


@app.route('/runs')
def runs():
    G = semacs.io.load()
    runs = [d for n, d in G.nodes_iter(data=True) if d["type"] == "run"]
    return render_template("runs.html", runs=runs)


@app.route("/tags")
def tags():
    G = semacs.io.load()
    tags = [d for n, d in G.nodes_iter(data=True) if d["type"] == "tag"]
    return render_template("tags.html", tags=tags)


@app.route("/ipynbs")
def ipynbs():
    G = semacs.io.load()
    ipynbs = [d for n, d in G.nodes_iter(data=True) if d["type"] == "ipynb"]
    for n in ipynbs:
        n["url"] = semacs.ipynb.get_url(n["path"])
    return render_template("ipynbs.html", ipynbs=ipynbs)


@app.route("/graph")
def graph():
    return render_template("graph.html")


@app.route("/json")
def json():
    return jsonify(semacs.io.load_obj())


@app.route('/node/<path:path>')
def node(path):
    path = "/" + path
    G = semacs.io.load()
    if path not in G.node:
        return "Not found: path=" + path
    node = G.node[path]
    non_seq, seq = semacs.utility.detect_sequence(os.listdir(path))
    dirs = sorted(filter(lambda p: op.isdir(op.join(path, p)), non_seq))
    files = [(p, semacs.utility.inspect_filetype(p), semacs.utility.strftime(op.join(path, p)))
             for p in non_seq if op.isfile(op.join(path, p))]
    files = sorted(files, key=lambda t: t[2])
    return render_template("dir_node.html", node=node, dirs=dirs, files=files)

if __name__ == '__main__':
    app.debug = True
    app.run()
