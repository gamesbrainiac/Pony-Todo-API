# encoding=utf-8
# app.py
__author__ = "Quazi Nafiul Islam"

import json

from flask import Flask, request
import flask.ext.restful as rest

from models import *

# Boilerplate
app = Flask(__name__)
api = rest.Api(app)

# Binding and generating mapping
db.bind('sqlite', 'todo_api.db', create_db=True)
db.generate_mapping(create_tables=True)


# Resource #######################################################################
class Todos(rest.Resource):

    def get(self):
        """Will give you all the todo items"""

        with orm.db_session:
            return {
                item.id: {
                    'task' : item.data,
                    'tags' : [tag.get_url() for tag in item.tags]
                }
                for item in Todo.select()
            }

    def put(self):
        """Payload contains information to create new todo item"""

        info = json.loads(request.data)

        with orm.db_session:
            item = Todo(data=info['data'])
            
            for tag_name in info['tags']:
                tag = Tag.get(name=tag_name)
                if tag is None:
                    tag = Tag(name=tag_name)
                item.tags += tag

        return {}, 200


class TodoItem(rest.Resource):

    def get(self, todo_id):
        """
        Get specific information on a Todo item

        :param todo_id: The Todo Item's ID, which is unique and a primary key
        :type todo_id: int
        """

        try:
            with orm.db_session:
                todo = Todo[todo_id]
                tags = list(todo.tags.name)

                return {
                    "task": todo.data,
                    "tags": tags
                }

        except orm.ObjectNotFound:
            return {}, 404


class Tags(rest.Resource):

    def get(self):
        """Will show you all tags"""

        with orm.db_session:
            return {
                tag.name: tag.get_url()
                for tag in Tag.select()
            }


class TagItem(rest.Resource):

    def get(self, tag_id):
        """
        Will show you information about a specific tag

        :param tag_id: ID for the tag
        :type tag_id: int
        """

        try:
            with orm.db_session:
                tag = Tag[tag_id]
                todos = list(tag.todos.data)

                return {
                    "tag": tag.name,
                    "tasks": todos
                }

        except orm.ObjectNotFound:
            return {}, 404

# Paths ##########################################################################
api.add_resource(Todos, '/', endpoint='Home')
api.add_resource(TodoItem, '/<int:todo_id>', endpoint='TodoItem')
api.add_resource(Tags, '/tags/', endpoint='Tags')
api.add_resource(TagItem, '/tags/<int:tag_id>', endpoint='TagItem')


if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True)