#!flask/bin/python
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/getProviders', methods=['GET'])
def get_providers():
    scope = request.args.get('scope')
    entity_type = request.args.get('entity')
    xml_string = getProviders.get_providers(scope, entity_type)
    return jsonify({'providers': xml_string})

if __name__ == '__main__':
    app.run(threaded=True)
