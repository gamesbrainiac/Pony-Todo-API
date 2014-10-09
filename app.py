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

        try:
            with po.db_session:

                return {
                    i.id: [
                        i.data,
                        ["http://localhost:5000/tags/{}".format(t.id) for t in i.tags]
                    ]
                    for i in po.select(item for item in Todo)
                }
        except Exception:
            return {}, 404

    def put(self):
        """Payload contains information to create new todo item"""

        info = json.loads(request.data)

        with po.db_session:
            item = Todo(data=info['data'])
            created_tags = {
                t.name: t
                for t in po.select(tag for tag in Tag)}

            for tag in info['tags']:
                if tag in created_tags:
                    item.tags += [created_tags[tag]]
                else:
                    item.tags += Tag(name=tag)

        return {}, 200


class TodoItem(rest.Resource):

    def get(self, todo_id):
        """
        Get specific information on a Todo item

        :param todo_id: The Todo Item's ID, which is unique and a primary key
        :type todo_id: int
        """

        with po.db_session:
            todo = po.select(x for x in Todo if x.id == todo_id)[:][0]

            todo_tag_ids = [tag.id for tag in todo.tags]

            tags = [
                tag.name for tag in
                po.select(t for t in Tag if t.id in todo_tag_ids)
            ]

            return {
                "Task": todo.data,
                "Tags": tags
            }


class Tags(rest.Resource):

    def get(self):
        """Will show you all tags"""

        with po.db_session:
            return {
                t.name: "http://localhost:5000/tags/{}".format(t.id)
                for t in po.select(_ for _ in Tag)
            }


class TagItem(rest.Resource):

    def get(self, tag_id):
        """
        Will show you information about a specific tag

        :param tag_id: ID for the tag
        :type tag_id: int
        """

        with po.db_session:
            tag = po.select(t for t in Tag if t.id == tag_id)[:][0]

            tag_todo_ids = [todo.id for todo in tag.todos]

            todos = [
                todo.data for todo in
                po.select(t for t in Todo if t.id in tag_todo_ids)
            ]

            return {
                "Tag": tag.name,
                "Todos": todos
            }

# Paths ##########################################################################
api.add_resource(Todos, '/', endpoint='Home')
api.add_resource(TodoItem, '/<int:todo_id>', endpoint='TodoItem')
api.add_resource(Tags, '/tags/', endpoint='Tags')
api.add_resource(TagItem, '/tags/<int:tag_id>', endpoint='TagItem')


if __name__ == '__main__':
    po.sql_debug(True)
    app.run(debug=True)