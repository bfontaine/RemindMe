# -*- coding: UTF-8 -*-

from flask import Flask, render_template, g, request
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from webassets_iife import IIFE
from remindme import store
from remindme.flaskutils import logged_only, unlogged_only, redirect_for

app = Flask(__name__)
app.config.from_pyfile('remindme.cfg', silent=True)

# i18n
babel = Babel(app)

# assets
assets = Environment(app)

# - JS
js = Bundle('js/jquery.js',
        #   'js/html5shiv.js',
        #   'js/icheck.min.js',
        #   'js/bootstrap.min.js',
            'js/app.js',
            filters=(IIFE, 'closure_js'), output='rm.js')
assets.register('js_all', js)

# - CSS
css = Bundle('css/bootstrap.min.css',
             'css/bootflat.min.css',
             'css/app.css',
             filters=('cssmin',), output='rm.css')
assets.register('css_all', css)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/home')
@logged_only
def app_index():
    # TODO
    return render_template('app_main.html')


@app.route('/login', methods=['GET', 'POST'])
@unlogged_only
def login():
    if request.method == 'POST':
        pass  # TODO
    else:
        return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
@unlogged_only
def signin():
    if request.method == 'POST':
        email  = request.form['email']

        if store.get_user(email=email):
            return 'already taken'  # TODO

        api_user = request.form['api_user']
        api_pass = request.form['api_pass']

        if store.get_user(api_user=api_user, api_pass=api_pass):
            return 'already taken'  # TODO

        passwd = request.form['password']

        return 'ok'  # TODO
    else:
        return render_template('signin.html')


@app.route('/logout', methods=['POST'])
@logged_only
def logout():
    g.user = None
    redirect_for('index')
