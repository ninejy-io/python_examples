# -*- coding: utf-8 -*-
import os, time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def get_page(url):
    print('<%s> is getting [%s]' % (os.getpid(), url))
    res = requests.get(url)
    if res.status_code == 200:
        return {'url': url, 'text': res.text}


def parse_page(res):
    res = res.result()
    print('<%s> is getting [%s]' % (os.getpid(), res['url']))
    with open('result.txt', 'a') as fd:
        parse_res = 'url: %s, size: %s\n' % (res['url'], len(res['text']))
        fd.write(parse_res)


if __name__ == '__main__':
    start = time.time()
    pool = ThreadPoolExecutor()
    # pool = ProcessPoolExecutor()
    urls = [
        'https://www.baidu.com',
        'http://www.qq.com',
        'https://www.jd.com',
        'http://www.sina.com.cn'
    ]

    for url in urls:
        pool.submit(get_page, url).add_done_callback(parse_page)

    pool.shutdown(wait=True)

    print('主: ', os.getpid(), ' total_time: ', (time.time() - start))
