#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)


@app.route('/')
def root():
    return "This is root!"

if __name__ == '__main__':
    app.run()
