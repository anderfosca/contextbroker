#!flask/bin/python
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", broker_url="http://localhost:5000")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=2000)
