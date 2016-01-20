#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("layout.html")


@app.route('/runs')
def runs():
    return "Run Lists"


@app.route("/projects")
def projects():
    return "Project Lists"


@app.route("/ipynbs")
def ipynbs():
    return "IPython Notebooks"

if __name__ == '__main__':
    app.debug = True
    app.run()
