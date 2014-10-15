# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

from pony import orm
from werkzeug.utils import cached_property

from TodoApp.Models import db


class Tag(db.Entity):
    _table_ = 'Tags'

    name = orm.Required(unicode, unique=True)
    todos = orm.Set("Todo")

    @cached_property
    def url(self):
        return "http://localhost:5000/tags/{}".format(self.id)