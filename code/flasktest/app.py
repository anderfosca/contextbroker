#!flask/bin/python
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
import MySQLdb
import sys

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/getProviders', methods=['GET'])
def get_tasks():
    return jsonify({'providers': tasks})

@app.route('/advertisement', methods=['POST'])
def adv():
    #root = ET.fromstring(request.data)
    #adv(root)
    #return codigo de erro, sucesso, etc
    return jsonify({'adv': request.data})

@app.route('/getContext', methods=['GET'])
def get_context():
    return jsonify({'providers': tasks})




if __name__ == '__main__':
    app.run(debug=True)
