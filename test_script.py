# encoding=utf-8
__author__ = "Quazi Nafiul Islam"

import os
import json
from pprint import pprint

import requests

username = 'gamesbrainiac'
password = 'islam'
name = 'nafiul'


def jsonify(obj):
    return json.dumps(obj)

try:
    # Creating a user
    data = requests.put('http://localhost:5000/user/',
                        data=jsonify({
                            'name': name,
                            'username': username,
                            'password': password}))

    pprint(data.text)

    # Getting token
    data = requests.post('http://localhost:5000/user/',
                         data=jsonify({
                             "username": username,
                             "password": password
                         }))

    pprint(data.text)

    # Getting token
    token = json.loads(data.text)['token']

    for var in 'cake sandwich computer laptop mouse plane'.split():

        data = requests.put('http://localhost:5000/',
                            data=jsonify({
                                'token': token,
                                'data': "Make a {}".format(var),
                                'tags': ['hello', 'world']
                            }))

        pprint(data.text)

    data = requests.get('http://localhost:5000/', data=jsonify({
        "token": token
    }))
    pprint(data.text)


except KeyboardInterrupt:
    os.remove('todo_api.db')