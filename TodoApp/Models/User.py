# encoding=utf-8

__author__ = "Quazi Nafiul Islam"

from flask import current_app
from pony import orm
import werkzeug.security as sec
import itsdangerous as danger

from . import db


class User(db.Entity):
    name = orm.Required(str, 64)

    usernname = orm.Required(str, 64)
    pass_hash = orm.Required(str, 128)

    todos = orm.Set("Todo")

    def set_pass_hash(self, password):
        self.pass_hash = sec.generate_password_hash(password)

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
        except danger.BadData:
            return None
        with orm.db_session:
            return User[data['id']]