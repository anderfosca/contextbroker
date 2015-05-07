#!flask/bin/python
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
import MySQLdb
import sys
import getProviders
import advertisement

broker = Flask(__name__)


@broker.route('/getProviders', methods=['GET'])
def get_providers():
    xml_string = getProviders.get_providers()
    return jsonify({'providers': xml_string})


@broker.route('/advertisement', methods=['POST'])
def register_broker():
    broker_info = request.data
    message = advertisement.register_broker(broker_info)
    # return codigo de erro, sucesso, etc
    return jsonify({'result': message})


@broker.route('/getContext', methods=['GET'])
def get_context():
    return jsonify({'result': ""})


@broker.route('/subscribe', methods=['POST'])
def subscribe():
    return jsonify({'result': ""})


@broker.route('/update', methods=['POST'])
def context_update():
    return jsonify({'result': ""})

if __name__ == '__main__':
    broker.run(debug=True)
