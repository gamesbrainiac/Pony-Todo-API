# encoding=utf-8
from TodoApp.Models.User import User

__author__ = "Quazi Nafiul Islam"

import flask_restful as rest
from flask import g
from pony import orm

from TodoApp.Models.Tag import Tag


class Tags(rest.Resource):
    def get(self):
        """Will show you all tags"""

        with orm.db_session:
            return {
                tag.name: tag.url
                for tag in User[g.user].tags
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