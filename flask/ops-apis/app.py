import json
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from utils.func import check_nginx_config, update_nginx_config
from config import BASE_DIR
import log

app = Flask(__name__)


@app.route('/checkconfig', methods=['POST'])
def check_config():
    json_data = json.loads(request.data.decode())
    if check_nginx_config(**json_data):
        return jsonify({"code": "0", "msg": "success"})
    return jsonify({"code": "30001", "msg": "nginx configuration has syntax error"})


@app.route('/updateconfig', methods=['POST'])
def update_config():
    json_data = json.loads(request.data.decode())
    if update_nginx_config(**json_data):
        return jsonify({"code": "0", "msg": "success"})
    return jsonify({"code": "30002", "msg": "nginx configuration update failed"})


if __name__ == "__main__":
    log.init_log(BASE_DIR + '/logs/api-server')
    print('Server start on 0.0.0.0:8000 ...')
    server = WSGIServer(('0.0.0.0', 8000), app)
    server.serve_forever()