# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

from pony import orm

db = orm.Database()


class Todo(db.Entity):
    _table_ = 'Todos'

    data = orm.Required(unicode)
    tags = orm.Set("Tag")


class Tag(db.Entity):
    _table_ = 'Tags'

    name = orm.Required(unicode, unique=True)
    todos = orm.Set("Todo")

    @property
    def url(self):
        return "http://localhost:5000/tags/{}".format(self.id)