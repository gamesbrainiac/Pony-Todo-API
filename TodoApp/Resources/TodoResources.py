# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

import json

from flask import request

from pony import orm
import flask_restful as rest

from TodoApp.Models.Tag import Tag
from TodoApp.Models.Todo import Todo


class Todos(rest.Resource):
    def get(self):
        """Will give you all the todo items"""

        with orm.db_session:
            return {
                item.id: {
                    'task': item.data,
                    'tags': [tag.url for tag in item.tags]
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
                tags = [{tag.name: tag.url} for tag in todo.tags]

                return {
                    "task": todo.data,
                    "tags": tags
                }

        except orm.ObjectNotFound:
            return {}, 404

    def delete(self, todo_id):

        try:
            with orm.db_session:
                todo = Todo[todo_id]

                if todo:
                    tags = todo.tags.copy()
                    todo.delete()

                    for tag in tags:
                        if not tag.todos:
                            tag.delete()
        except orm.ObjectNotFound:
            return {}, 400

        return {}, 200