# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

import json

from flask import request
from pony import orm
import flask.ext.restful as rest

from TodoApp.Models.User import User


class UserLogin(rest.Resource):
    def post(self):
        """Payload contains username and password"""

        info = json.loads(request.data)
        try:
            username = info['username']
            password = info['password']
        except KeyError, e:
            return {"auth_error": "Username and/or Password invalid"}

        with orm.db_session:
            u = User.get(username=username)
            if u:
                if u.verify_password(password):
                    return {"token": u.generate_auth_token()}, 200
                else:
                    return {"error": "Your password is incorrect"}, 401
            else:
                return {"error": "Your username does not exist"}, 401

    def put(self):
        info = json.loads(request.data)

        try:
            name = info['name']
            username = info['username']
            password = info['password']
        except KeyError, e:
            return {}, 404

        with orm.db_session:
            try:
                u = User.get(username=username)
                if not u:
                    u = User(name=name, username=username,
                             pass_hash=User.set_pass_hash(password))
                    u.set_pass_hash(password)
            except orm.ObjectNotFound:
                return {"error": "We made a mistake"}, 404
            return {"Success": "Success"}, 200