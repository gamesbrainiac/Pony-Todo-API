# encoding=utf-8

__author__ = "Quazi Nafiul Islam"

from flask import current_app
from pony import orm
import werkzeug.security as sec
import itsdangerous as danger

from . import db


class User(db.Entity):
    """
    A user class that inherits from db.Entity, where db is an instance of
    pony.orm.Database.

    :param name: The name of the user e.g. John Doe
    :type name: str

    :param username: The username of the user, e.g. jdoe
    :type username: str

    :param pass_hash: The password hash, not directly put into an initializer,
     use set_pass_hash instead.
    :type pass_hash: str

    :param Todos: A set of todos
    :type todos: set
    """
    name = orm.Required(str, 64)

    username = orm.Required(str, 64)
    pass_hash = orm.Required(str, 128)

    todos = orm.Set("Todo")

    @staticmethod
    def set_pass_hash(password):
        return sec.generate_password_hash(password)

    def verify_password(self, password):
        return sec.check_password_hash(self.pass_hash, password)

    def generate_auth_token(self, expires_in=3600):

        s = danger.TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], salt='nobodyknows', expires_in=expires_in
        )

        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = danger.TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], salt='nobodyknows')
        try:
            data = s.loads(token)
            return data
        except danger.BadData:
            return None