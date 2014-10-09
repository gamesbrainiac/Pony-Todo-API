# encoding=utf-8
# models.py
__author__ = "Quazi Nafiul Islam"

import pony.orm as po

db = po.Database()


class Todo(db.Entity):

    _table_ = 'Todos'

    data = po.Required(unicode)
    tags = po.Set("Tag")


class Tag(db.Entity):

    _table_ = 'Tags'

    name = po.Required(unicode)
    todos = po.Set("Todo")

    def get_url(self):
        return "http://localhost:5000/tags/{}".format(self.id)
