# -*- coding: utf-8 -*-
from gevent import spawn, joinall, monkey; monkey.patch_all()
import time
import requests
from threading import current_thread


def parse_page(res):
    print('%s PARSE %s' % (current_thread().getName(), len(res)))


def get_page(url, callback=parse_page):
    print('%s GET %s' % (current_thread().getName(), url))
    res = requests.get(url)
    if res.status_code == 200:
        callback(res.text)


if __name__ == '__main__':
    start = time.time()
    urls = [
        'https://www.baidu.com',
        'https://www.taobao.com',
        'https://www.openstack.org',
        'https://www.docker.com'
    ]

    tasks = []
    for url in urls:
        tasks.append(spawn(get_page, url))

    joinall(tasks)
    print('total_time: ', (time.time() - start))
