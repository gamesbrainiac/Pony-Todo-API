# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

from pony import orm

from TodoApp.Models import db


class Todo(db.Entity):

    _table_ = 'Todos'

    user = orm.Required("User")
    data = orm.Required(unicode)
    tags = orm.Set("Tag")