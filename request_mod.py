# encoding=utf-8
import json

from pony import orm

from TodoApp.Models.User import User


__author__ = "Quazi Nafiul Islam"

from flask import request, g


def before_request():
    """
    Checks if there is a token before letting client access any path
    other than `/user/`
    """
    path = request.path

    if path != '/user/':
        try:
            with orm.db_session:
                token = json.loads(request.data)['token']
                user = User.verify_auth_token(token)['id']
                if user:
                    g.user = user
                else:
                    g.user = None
        except (orm.ObjectNotFound, TypeError, KeyError):
            pass


def after_request(response):
    try:
        g.user = None
    except AttributeError:
        pass
    return response