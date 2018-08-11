# coding:utf-8
import os
import docker
import sqlite3
import hashlib
import requests
from datetime import datetime
from flask_login import UserMixin


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = CUR_DIR + '/' + 'sqlite.db'
docker_file_path = '/opt/test/'


class DockerManager(object):
    def __init__(self):
        super(DockerManager, self).__init__()
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def get_all_container(self):
        return [{'name': i.name, 'ID': i.short_id, 'image': i.image.tags[0], 'status': i.status} for i in self.client.containers.list(all=True)]

    def run_con(self, image, **kwargs):
        self.client.containers.run(image=image, **kwargs)

    def start(self, name):
        self.client.containers.get(name).start()

    def stop(self, name):
        self.client.containers.get(name).stop(timeout=60)

    def delete(self, name):
        self.client.containers.get(name).remove()

    def get_images(self):
        images = []
        for i in self.client.images.list():
            if i.tags:
                images.append({'Id': i.short_id.split(':')[1], 'Tag': i.tags[0]})
        return images

    def build_image(self, **kwargs):
        data = {
            "path": docker_file_path,
            "tag": kwargs['tag'],
            "nocache": False,
            "quiet": False,
            "timeout": 60,
            "encoding": "gzip",
            "forcerm": True
        }
        try:
            image = self.client.images.build(**data).tags[0]
        except Exception:
            image = 'error'
        return image

    def pull_image(self, name, tag=None, **kwargs):
        try:
            image = self.client.images.pull(name, tag, **kwargs).tags[0]
        except Exception:
            image = 'error'
        return image

    def push_image(self, repository, tag=None, **kwargs):
        # This just a example
        # kwargs['auth_config'] = {'username': 'admin', 'password': '123456'}
        kwargs['stream'] = True
        self.client.images.push(repository, tag, **kwargs)

    def remove_image(self, *args, **kwargs):
        self.client.images.remove(*args, **kwargs)


class DbManager(object):
    def __init__(self):
        super(DbManager, self).__init__()
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def query(self, sql, *args):
        self.cursor.execute(sql, *args)
        return self.cursor.fetchall()

    def exec_sql(self, sql, *args):
        self.cursor.execute(sql, *args)
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class User(UserMixin):
    @property
    def is_authenticated(self):
        return True

    @property
    def is_actice(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return "100"


def check_user(user, pwd):
    db = DbManager()
    cur_pwd = hashlib.md5(pwd).hexdigest()
    sql = "select pwd from user_info where user = ?;"
    try:
        res = db.query(sql, (user,))[0][0]
    except Exception:
        res = None
    if res is not None and res == cur_pwd:
        result = True
    else:
        result = False
    return result


def user_register(user, pwd):
    db = DbManager()
    sql = "insert into user_info (user, pwd) values (?, ?);"
    try:
        db.exec_sql(sql, (user, hashlib.md5(pwd).hexdigest(),))
        return True
    except Exception:
        return False


def check_image_tag(name, tag):
    url = 'https://docker-registry.example.com'
    auth = ('admin', '123456')
    r = requests.get(url + '/v2/' + name + '/tags/list', auth=auth)
    if tag in r.json()['tags']:
        return True
    return False


def record_image_info(tag, image):
    sql = "insert into tags (tag, image, build_time) values (?, ?, ?);"
    db = DbManager()
    try:
        db.exec_sql(sql, (tag, image, datetime.now(),))
    except Exception:
        pass


def get_all_images_info():
    db = DbManager()
    return db.query("select * from tags;")


def delete_image_info(image):
    db = DbManager()
    try:
        db.exec_sql("delete from tags where image = ?", (image,))
    except Exception:
        pass


# db = DbManager()
# user_sql = "CREATE TABLE user_info (user varchar(50), pwd varchar(50));"
# tags_sql = "CREATE TABLE tags (tag varchar(50), image varchar(255), build_time varchar(50));"
# db.exec_sql(tags_sql, ('1.0.1', 'php', datetime.now(),))
