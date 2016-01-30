#!/usr/bin/env python
# -*- coding: utf-8 -*-

import semacs
from flask import Flask, render_template, jsonify
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
    return render_template("dir_node.html", node=node)

if __name__ == '__main__':
    app.debug = True
    app.run()
