#!flask/bin/python
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
import MySQLdb
import sys
import getProviders
import advertisement
import getContext
import subscription
import update

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
    result = getContext.get_context()
    return jsonify({'result': result})


@broker.route('/subscribe', methods=['POST'])
def subscribe():
    result = subscription.subscribe(request.data, request.data)
    return jsonify({'result': result})


@broker.route('/update', methods=['POST'])
def context_update():
    result = update.context_update(request.data)
    return jsonify({'result': result})

if __name__ == '__main__':
    broker.run(debug=True)
