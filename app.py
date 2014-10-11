# encoding=utf-8
# app.py

__author__ = "Quazi Nafiul Islam"

from flask import Flask
import flask_restful as rest
from pony import orm

from TodoApp.Models import db
from TodoApp.Resources.TagResources import Tags, TagItem
from TodoApp.Resources.TodoResources import Todos, TodoItem


# Boilerplate
app = Flask(__name__)
api = rest.Api(app)

# Binding and generating mapping
db.bind('sqlite', 'todo_api.db', create_db=True)
db.generate_mapping(create_tables=True)

# Registering resources
api.add_resource(Todos, '/', endpoint='Home')
api.add_resource(TodoItem, '/<int:todo_id>', endpoint='TodoItem')
api.add_resource(Tags, '/tags/', endpoint='Tags')
api.add_resource(TagItem, '/tags/<int:tag_id>', endpoint='TagItem')

if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True)