# -*- coding: UTF-8 -*-

from flask import g, redirect, url_for

def user():
    """
    Return the currently connected user
    """
    return getattr(g, 'user', None)


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


def redirect_for(s, code=302):
    return redirect(url_for(s, code))
