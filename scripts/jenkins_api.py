import json
import requests


jenkins_url = "http://xxxx"
auth = ('admin', 'admin')
headers = {"Jenkins-Crumb": "e1d6612435c719a4a92285b4c441a1c9"}

s = requests.Session()
s.auth = auth


def get_crumb():
    url = f"{jenkins_url}/crumbIssuer/api/json"
    r = s.get(url)
    print(r.json())


def create_job(name):
    url = f"{jenkins_url}/createItem?name={name}"  ##&from=ansible-deploy&mode=copy
    headers.update({"Content-Type": "text/xml"})
    config_xml = open('config.xml', 'rb').read()
    r = s.post(url, data=config_xml, headers=headers)
    print(r.status_code)


def update_job(name):
    url = f"{jenkins_url}/job/{name}/config.xml"
    headers.update({"Content-Type": "text/xml"})
    config_xml = open('config.xml', 'rb').read()
    r = s.post(url, data=config_xml, headers=headers)
    print(r.status_code)


def delete_job(name):
    url = f"{jenkins_url}/job/{name}/doDelete"
    r = s.post(url, headers=headers)
    print(r.status_code)


def build_job(name, params_dict):
    '''
    params_dict = {
        "ENV": "beta",
        "app_id": "aaa",
        "server_type": "ccc",
        "tag_name": "eee"
    }
    '''
    url = f"{jenkins_url}/job/{name}/buildWithParameters"
    headers.update({"Content-Type": "application/x-www-form-urlencoded"})
    r = s.post(url, data=params_dict, headers=headers)
    print(r.status_code, r.content)


def get_job_info(name):
    url = f"{jenkins_url}/job/{name}/api/json"
    r = s.get(url)
    print(r.status_code, r.json())

