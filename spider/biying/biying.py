import os
import re
import requests
import time


base_url = "https://cn.bing.com/"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
re_img = re.compile(r'g_img={url: "(.*?)"')


def get_biying_index_image(zh=True):
    os.path.exists('images') or os.mkdir('images')
    file_name = 'images/biying_' + str(int(time.time())) + '.jpg'
    index_url = base_url if zh else base_url + '?ensearch=1'

    r = requests.get(index_url, headers=headers)

    for img_url in re.findall(re_img, r.content):
        res = requests.get(base_url + img_url, headers=headers)
        with open(file_name, 'ab+') as fd:
            for chunk in res.iter_content(chunk_size=1024):
                fd.write(chunk)


if __name__ == '__main__':
    get_biying_index_image()
    time.sleep(2)
    get_biying_index_image(zh=False)
