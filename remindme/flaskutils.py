# -*- coding: UTF-8 -*-

from flask.ext.babel import gettext
from flask import g, redirect, url_for, session


def user():
    """
    Return the currently connected user
    """
    return getattr(g, 'user', None)


###############################################################################
# Redirections
###############################################################################

def _redirect_cond(cond, url_str, name):
    def _deco(fun):
        def _fun(*args, **kwargs):
            if cond():
                return redirect(url_for(url_str))
            return fun(*args, **kwargs)
        _fun.__name__ = fun.__name__
        return _fun
    _deco.__name__ = name
    return _deco

# decorator: redirect to /login if user is not logged in
logged_only = _redirect_cond(lambda: user() is None, 'login', 'logged_only')

# decorator: redirect to / if user is logged in
unlogged_only = _redirect_cond(lambda: user(), 'app_index', 'unlogged_only')


def redirect_for(s, args=None, code=302):
    """
    Shortcut for ``redirect(url_for(s), code)``. The second argument can be
    used to transmit args to the redirected view using ``store_session``.
    """
    if args:
        store_session(args, s)
    return redirect(url_for(s), code)


###############################################################################
# Session management
###############################################################################

def store_session(args, token):
    """
    Store something (``args``) in the session, using ``token`` as an unique
    identifier.
    """
    session.setdefault('args', {})
    session['args'][token] = args


def retrieve_session(token):
    """
    Retrieve data from the session, as stored by ``store_session``. This
    returns ``None`` if this token doesn't has data in this session.
    """
    if 'args' in session:
        return session['args'].pop(token, None)


###############################################################################
# Debugging
###############################################################################

def set_debug_mode(is_on):
    """
    Set ``g.debug_mode`` based on ``is_on``.
    """
    setattr(g, 'debug_mode', bool(is_on))


def is_debug_mode():
    """
    Check if we're in "debug" mode
    """
    return getattr(g, 'debug_mode', False)


###############################################################################
# Templates
###############################################################################

def setvar(name, value):
    """
    decorator to set a variable on 'g'
    """
    def _deco(fun):
        def _fun(*args, **kwargs):
            _value = gettext(value) if isinstance(value, str) else value
            setattr(g, name, _value)
            return fun(*args, **kwargs)

        _fun.__name__ = fun.__name__
        return _fun

    return _deco

# shortcut
title = lambda v: setvar('title', v)
