# encoding=utf-8
# app.py

__author__ = "Quazi Nafiul Islam"

# Flask imports
from flask import Flask
import flask_restful as rest
from pony import orm

# App Imports
from TodoApp.Models import db
from TodoApp.Resources.TagResources import Tags, TagItem
from TodoApp.Resources.TodoResources import Todos, TodoItem

# Setting imports from ./settings.py
import settings

# Boilerplate
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY

api = rest.Api(app)

# Binding and generating mapping
db.bind(settings.DBTYPE, settings.DBNAME, create_db=True)
db.generate_mapping(create_tables=True)

# Registering resources
api.add_resource(Todos, '/', endpoint='Home')
api.add_resource(TodoItem, '/<int:todo_id>', endpoint='TodoItem')
api.add_resource(Tags, '/tags/', endpoint='Tags')
api.add_resource(TagItem, '/tags/<int:tag_id>', endpoint='TagItem')

if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True)