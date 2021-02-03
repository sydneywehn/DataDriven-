from flask import Flask, jsonify
from db import execute_list_query

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(test())


if __name__ == '__main__':
    app.run()
