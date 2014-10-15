# encoding=utf-8
# app.py

__author__ = "Quazi Nafiul Islam"

# stdlib imports
import os

# Flask imports
from flask import Flask
import flask_restful as rest
from pony import orm

# App Imports
from TodoApp.Models import db
from TodoApp.Resources.LoginResources import UserLogin
from TodoApp.Resources.TagResources import Tags, TagItem
from TodoApp.Resources.TodoResources import Todos, TodoItem
import request_mod as rm

# Setting imports from ./settings.py
import settings

# Boilerplate
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
api = rest.Api(app)


# Request configuration
app.before_request(rm.before_request)
app.after_request(rm.after_request)


# Binding and generating mapping
if settings.DBNAME in os.listdir('.'):
    os.remove(settings.DBNAME)
db.bind(settings.DBTYPE, settings.DBNAME, create_db=True)
db.generate_mapping(create_tables=True)

# Registering resources
api.add_resource(UserLogin, '/user/', endpoint='login')
api.add_resource(Todos, '/', endpoint='Home')
api.add_resource(TodoItem, '/<int:todo_id>', endpoint='TodoItem')
api.add_resource(Tags, '/tags/', endpoint='Tags')
api.add_resource(TagItem, '/tags/<int:tag_id>', endpoint='TagItem')

if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True)
    # app.run(debug=False)