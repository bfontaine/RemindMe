# -*- coding: UTF-8 -*-

from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from webassets_iife import IIFE

app = Flask(__name__)

# assets
assets = Environment(app)

# - JS
js = Bundle(
            filters=(IIFE, 'closure_js'), output='rm.js')
assets.register('js_all', js)

# - CSS
css = Bundle(
             filters=('cssmin',), output='rm.css')
assets.register('css_all', css)


@app.route('/')
def index():
    return render_template('main.html')
