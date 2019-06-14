import time
from datetime import datetime, timedelta
import requests

'''
<<无名之辈>>影评 来自猫眼电影
'''


def get_data(url):
    headers = {
        "Host": "m.maoyan.com",
        "Referer": "http://m.maoyan.com/movie/1208282/comments?_v_=yes",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }
    data = []
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["cmts"]
    else:
        return None


def parse_data(data):
    comments = []
    try:
        for item in data:
            comment = {
                "nickName": item["nickName"],
                "cityName": item["cityName"] if "cityName" in item else "",
                "content": item["content"].strip().replace("\n", ""),
                "score": item["score"],
                "startTime": item["startTime"]
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)


def save_data(comments):
    with open('comments.txt', 'a+', encoding='utf-8') as fd:
        for i in comments:
            fd.write(i['nickName'] + ',' + i['cityName'] + ',' + i['content'] + ',' + str(i['score']) + ',' + i['startTime'] + '\n')


def main():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = '2018-11-16 00:00:00'
    while start_time > end_time:
        url = "http://m.maoyan.com/mmdb/comments/movie/1208282.json?_v_=yes&offset=15&startTime=" + start_time
        data = None
        try:
            data = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            data = get_data(url)
        else:
            time.sleep(0.1)
        comments = parse_data(data)
        save_data(comments)
        start_time = comments[14]['startTime']
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        print(start_time)


if __name__ == "__main__":
    main()