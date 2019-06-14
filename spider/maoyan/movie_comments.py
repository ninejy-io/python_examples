import json
import requests
import time
from datetime import datetime, timedelta
from collections import Counter
from pyecharts import Geo, Bar
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "Referer": "http://m.maoyan.com/movie/42964/comments?_v_=yes"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get('cmts')
    return None


def parse_data(data):
    comments = []
    try:
        for item in data:
            comment = {
                "nickName": item["nickName"],
                "cityName": item["cityName"] if item.get("cityName") else "",
                "content": item["content"].strip().replace("\n", ""),
                "score": item["score"],
                "startTime": item["startTime"]
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)


def save_data(comments):
    with open('data/comments.txt', 'a+', encoding='utf-8') as fd:
        for c in comments:
            fd.write(c["nickName"]+','+c["cityName"]+','+c["content"]+','+str(c["score"])+','+c["startTime"]+'\n')


def hot_city():
    data = []
    cities = []
    city_counts = {}
    with open('data/comments.txt', 'r', encoding='utf-8')as f:
        rows = f.readlines()
        try:
            for row in rows:
                if row != '':
                    city = row.split(',')[1]
                if city != '':
                    cities.append(city)
                    if not city_counts.get(city):
                        city_counts[city] = 1
                    else:
                        city_counts[city] += 1
        except Exception as e:
            print(e)
    for k, v in city_counts.items():
        data.append((k, v))
    # print(data)
    # geo = Geo('Audiences distribution', 'Data Source: m.maoyan.com', title_color="#fff", title_pos="center", width=1000,
    #             height=600, background_color='#404a59')
    # attr, value = geo.cast(data)
    # geo.add('', attr, value, visual_range=[0, 1000], visual_text_color='#fff', symbol_size=15, is_visualmap=True,
    #         is_piecewise=False, visual_split_number=10)
    # geo.render('output/audiences-distribution.html')

    top20_cities = Counter(cities).most_common(20)
    bar = Bar('Top20 cities of audiences', 'Data Source: m.maoyan.com', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(top20_cities)
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render('output/Audiences-source.html')


def generate_wordcloud():
    comments = []
    with open('data/comments.txt', 'r', encoding='utf-8') as f:
        rows = f.readlines()
        try:
            for row in rows:
                comment = row.split(',')[2]
                if comment != '':
                   comments.append(comment)
        except Exception as e:
            print(e)
    comment_after_split = jieba.cut(str(comments), cut_all=False)
    words = ' '.join(comment_after_split)
    stopwords = STOPWORDS.copy()
    stopwords.add('电影')
    stopwords.add('一部')
    stopwords.add('一个')
    stopwords.add('没有')
    stopwords.add('什么')
    stopwords.add('有点')
    stopwords.add('感觉')
    stopwords.add('毒液')
    stopwords.add('就是')
    stopwords.add('觉得')
    bg_image = plt.imread('bg.jpg')
    wc = WordCloud(background_color='lightblue', mask=bg_image, font_path='STKAITI.TTF',
                   stopwords=stopwords, max_font_size=400, random_state=50)
    wc.generate_from_text(words)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = '2018-11-09 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=15&startTime=' + start_time.replace(' ', '%20')
        data = None
        try:
            data = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            data = get_data(url)
        else:
            time.sleep(0.1)

        if data is None:
            continue
        comments = parse_data(data)
        save_data(comments)
        start_time = comments[14]['startTime']
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        print(start_time)

    generate_wordcloud()
    hot_city()
