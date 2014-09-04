# -*- coding: UTF-8 -*-

from flask import Flask, render_template, g, request, flash, session
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel, gettext
from webassets_iife import IIFE

from remindme import ajax, store
from remindme.core import schedule_sms, SMSException
from remindme.flaskutils import logged_only, unlogged_only, redirect_for, \
        retrieve_session, user
from remindme.log import mkLogger

app = Flask(__name__)
app.config.from_pyfile('remindme.cfg', silent=True)

logger = mkLogger('app')

# i18n
babel = Babel(app)

# assets
assets = Environment(app)

# - JS
js = Bundle(
    # Bootstrap/Bootflat
    'js/vendor/jquery.js',
    'js/vendor/html5shiv.js',
   #'js/vendor/icheck.min.js',
    'js/vendor/bootstrap.min.js',
    'js/vendor/angular.js',
    'js/vendor/mousetrap.js',
    'js/vendor/wMousetrap.js',
    'js/vendor/ui-bootstrap-tpls-0.11.0.js',
    # Our JS
    'js/utils.js',
    'js/app.js',
    filters=(IIFE, 'closure_js') if not app.config['DEBUG'] else (),
    output='js/rm.js')
assets.register('js_all', js)

# - CSS
css = Bundle(
    # Bootstrap/Bootflat
    'css/bootstrap.min.css',
    'css/bootflat.min.css',
    # Our JS
    'css/app.css',
    filters=('cssmin',) if not app.config['DEBUG'] else (),
    output='css/rm.css')
assets.register('css_all', css)

@app.before_request
def set_current_user():
    _id = session.get('_id')
    if _id and '/static/' not in request.path:
        setattr(g, 'user', store.get_user(_id=_id))


@app.before_request
def set_g_locale():
    if '/static/' not in request.path:
        logger.debug("setting user locale...")
        setattr(g, 'locale', babel.locale_selector_func())


@babel.localeselector
def get_locale():
    trs = [str(t) for t in babel.list_translations()]
    # 1. ?locale=
    locale_param = request.args.get('locale') or request.args.get('lang')
    if locale_param:
        if locale_param[:2] in trs:
            logger.debug("Known locale param: %s", locale_param)
            return locale_param
        logger.debug("Unknown locale param: %s", locale_param)
    # 2. user.locale
    u = user()
    if u and u.locale:
        logger.debug("Using user locale")
        return u.locale
    # 3. request header
    logger.debug("locale: fall back in headers")
    return request.accept_languages.best_match(trs)


@app.route('/')
@unlogged_only
def index():
    return render_template('main.html')

@app.route('/home', methods=['GET', 'POST'])
@logged_only
def app_index():
    fields = retrieve_session('app_index')
    if request.method == 'POST':
        key, pswd = g.user.api_username, g.user.api_password
        try:
            schedule_sms(request.form['text'], request.form['when'],
                     {'user': key, 'pass': pswd})
        except SMSException as e:
            print e
            flash(gettext("Oops, error."), 'danger')
            return redirect_for('app_index')
        else:
            flash(gettext("Scheduled!"), 'success')
            return redirect_for('app_index')
    else:
        return render_template('app_main.html', fields=fields)


@app.route('/login', methods=['GET', 'POST'])
@unlogged_only
def login():
    err = gettext('Wrong email or password.')
    if request.method == 'POST':
        email = request.form['email']
        user = store.get_user(email=email)
        if not user or not user.check_password(request.form['password']):
            flash(err, 'danger')
            return redirect_for('login')
        session['_id'] = str(user._id)
        return redirect_for('app_index')
    fields = retrieve_session('login')
    return render_template('login.html', fields=fields)


@app.route('/signin', methods=['GET', 'POST'])
@unlogged_only
def signin():
    fields = retrieve_session('signin')
    if request.method == 'POST':
        email  = request.form['email']

        if store.get_user(email=email):
            flash(gettext('This email is already registered'), 'danger')
            return redirect_for('signin', request.form)

        api_user = request.form['api_user']
        api_pass = request.form['api_pass']

        if store.get_user(api_user=api_user, api_pass=api_pass):
            flash(gettext('These API credentials are already registered'), 'danger')
            return redirect_for('signin', request.form)

        passwd = request.form['password']

        user = store.User(email, passwd, api_user, api_pass)
        user.save()

        flash(gettext('Your account has been successfully created!'), 'success')
        return redirect_for('login', {'email': user.email})
    return render_template('signin.html', fields=fields)


@app.route('/logout', methods=['POST'])
@logged_only
def logout():
    g.user = None
    session.clear()
    return redirect_for('index')


## API
@app.route('/ajax/sms/schedule', methods=['POST'])
@logged_only
def ajax_sms_schedule(): # POST text (string), when (ISO date string)
    return ajax.api_schedule_sms(request.data)
