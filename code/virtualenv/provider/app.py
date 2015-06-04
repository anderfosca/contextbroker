#!flask/bin/python
__author__ = 'anderson'

from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

def advertise_f(xml_string, broker_url):
    target_url = broker_url+"/advertisement"
    r = requests.post(target_url, xml_string)
    return r.content

def update_f(xml_string, broker_url):
    target_url = broker_url+"/update"
    r = requests.post(target_url, xml_string)
    return r.content

@app.route('/advertise')
def advertise():
    xml_string= request.args.get('xml_string')
    broker_url = request.args.get('broker_url')
    result = advertise_f(xml_string,broker_url)
    return result

@app.route('/update')
def update():
    xml_string= request.args.get('xml_string')
    broker_url = request.args.get('broker_url')
    result = update_f(xml_string,broker_url)
    return result

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
    app.run( use_reloader=True, port=3000)
