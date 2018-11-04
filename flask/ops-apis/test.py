import requests


data = {
    "server_group_name": "nginx_test",
    "git_version": "master",
    "server_nodes": ['192.168.152.116', '192.168.152.145']
}


def test_check_nginx_config():
    r = requests.post('http://192.168.152.108:8000/checkconfig', json=data)
    print(r.content)


def test_update_nginx_config():
    r = requests.post('http://192.168.152.108:8000/updateconfig', json=data)
    print(r.content)


# test_check_nginx_config()
# test_update_nginx_config()