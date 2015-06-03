#!flask/bin/python
__author__ = 'anderson'

from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

@app.route('/advertise', methods=['GET'])
def advertise(url, xml):
    r = requests.post(url, xml)
    return r.json()

@app.route('/update', methods=['GET'])
def update(url, xml):
    r = requests.post(url, xml)
    return r.json()

@app.route('/getContext', methods=['GET'])
def getContext(url, xml):
    r = requests.post(url, xml)
    return r.json()

@app.route('/')
def index():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/adv.xml', 'r') as f:
        adv_xml= f.read()
    with open(os.path.dirname(os.path.abspath(__file__)) + '/upd.xml', 'r') as f:
        upd_xml= f.read()
    return render_template("index.html", broker_url="http://localhost:5000", adv_xml=adv_xml, upd_xml=upd_xml)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=3000)
