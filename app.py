# -*- coding: UTF-8 -*-

from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from webassets_iife import IIFE

app = Flask(__name__)
app.config.from_pyfile('remindme.cfg', silent=True)

# i18n
babel = Babel(app)

# assets
assets = Environment(app)

# - JS
js = Bundle(filters=(IIFE, 'closure_js'), output='rm.js')
assets.register('js_all', js)

# - CSS
css = Bundle(filters=('cssmin',), output='rm.css')
assets.register('css_all', css)


@app.route('/')
def index():
    return render_template('main.html')
