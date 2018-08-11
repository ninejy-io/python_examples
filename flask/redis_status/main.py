# coding: utf-8
from flask import Flask, request, url_for, render_template, jsonify
from utils import load_info


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('info.html')


@app.route('/get_info')
def get_info():
    return jsonify(load_info())


if __name__ == '__main__':
    app.run('0.0.0.0', 9000)
