# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

from . import orm, db


class Todo(db.Entity):

    _table_ = 'Todos'

    data = orm.Required(unicode)
    tags = orm.Set("Tag")