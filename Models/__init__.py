# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

from pony import orm

db = orm.Database()

from Tag import Tag
from Todo import Todo

__all__ = ['orm', 'db', 'Tag', 'Todo']