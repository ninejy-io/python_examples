import time
import random
import requests
from lxml import etree


base_url = "http://www.xicidaili.com/"

deepth = 101

headers = {
    "Host": "www.xicidaili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

scheme_map = {
    "http": "wt",
    "https": "wn"
}

def get_ips(url):
    ips = []
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    try:
        for sub_html in html.xpath('//*[@id="ip_list"]/tr'):
            if isinstance(sub_html, list):
                if sub_html[0].tag == "th":
                    continue
                ip_port = '{}:{}'.format(sub_html[1].text, sub_html[2].text)
                ips.append(ip_port)
        print(len(ips))
        return ips
    except Exception as e:
        print(e)


def get_urls(scheme='http'):
    urls = []
    for i in range(1, deepth):
        url = base_url + scheme_map[scheme] + '/' + str(i)
        urls.append(url)
    return urls


def save_data(scheme):
    for url in get_urls(scheme):
        with open(scheme + '.txt', 'a+') as fd:
            for ip in get_ips(url):
                fd.write(ip + "\n")
        time.sleep(random.random())


if __name__ == "__main__":
    save_data('http')
    save_data('https')
