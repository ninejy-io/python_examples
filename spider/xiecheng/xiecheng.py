# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
from models import db, Urls, Hotel, Comments


region = 'shanghai2'
category = 'hotel'
base_url = 'http://hotels.ctrip.com'
deep = 51  # 爬取前50页的内容
delay = 5

try:
    db.connect()
    db.create_tables([Urls, Hotel, Comments])
except Exception:
    print 'Table had already exists...'

user_agent = (
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent
comments_driver = webdriver.PhantomJS(desired_capabilities=dcap)
comments_driver.set_window_size(1260, 7591)
url_driver = webdriver.PhantomJS(desired_capabilities=dcap)
url_driver.set_window_size(1260, 7591)


def _get_url_from_soup(soup):
    for hotel in soup.find_all(attrs={'class': 'hotel_name'}):
        if hotel.a:
            try:
                Urls.create(url=hotel.a['href'])
                # print hotel.a['href']
            except Exception, e:
                print hotel.a['href'], e


def get_url():
    url_driver.get(base_url + '/' + category + '/' + region)
    soup = BeautifulSoup(url_driver.page_source, 'html.parser')
    _get_url_from_soup(soup)
    for i in range(1, deep):
        try:
            url_driver.find_element_by_xpath(u'//*[@id="downHerf"]').click()
            time.sleep(delay)
            soup = BeautifulSoup(url_driver.page_source, 'html.parser')
            _get_url_from_soup(soup)
        except Exception:
            continue
    url_driver.close()


def _get_comments_from_soup(hotel_id, soup):
    for so in soup.find_all(attrs={'class': 'J_commentDetail'}):
        if so.text:
            try:
                Comments.create(hotel_id=hotel_id, comment=so.text.encode('utf-8'))
                # print so.text.encode('utf-8')
            except Exception, e:
                print so.text.encode('utf-8'), e


def get_comments():
    while True:
        try:
            url = Urls.select().where(Urls.status=='new').limit(1).get().url
            # print url
            if not url:
                break
            Urls.update(status='done').where(Urls.url==url).execute()
            hotel_id = url.split('/')[2].split('.')[0]
            comments_driver.get(base_url + url)
            soup = BeautifulSoup(comments_driver.page_source, 'html.parser')
            try:
                name = soup.find(attrs={'itemprop': 'name'}).text.encode('utf-8')
            except Exception, e:
                print "hotel name not found ", e
                name = hotel_id
            Hotel.create(hotel_id=hotel_id, hotel_name=name)
        except Exception, e:
            print "Insert into hotel error ", e
            Urls.update(status='new').where(Urls.url==url).execute()
            continue
        _get_comments_from_soup(hotel_id, soup)
        for i in range(1, deep):
            try:
                if not comments_driver.find_element_by_xpath(u'//*[@id="divCtripComment"]/div[5]/div/a[2]/span').click():
                    comments_driver.find_element_by_xpath(u'//*[@id="divCtripComment"]/div[4]/div/a[2]/span').click()
                time.sleep(delay)
                soup = BeautifulSoup(comments_driver.page_source, 'html.parser')
                _get_comments_from_soup(hotel_id, soup)
            except Exception, e:
                print "comments not found on page {}".format(str(i)), e
                continue
    comments_driver.close()


# get_url()
get_comments()
db.close()
