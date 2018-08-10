# -*- coding: utf-8 -*-
import time
import requests
import itchat
import random


def get_news():
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation


def send_news(name):
    try:
        itchat.auto_login(hotReload=True)
        my_friend = itchat.search_friends(name=name)
        user_name = my_friend[0]['UserName']

        messages = ["学习", "看电视", "打游戏", "运动", "旅游", "看书", "吃饭", "逛街", "唱歌", "跳舞"]

        itchat.send(random.choices(messages), toUserName=user_name)
    except Exception as e:
        print("{}".format(e))


if __name__ == '__main__':
    while True:
        send_news("xyz")
        time.sleep(300)
