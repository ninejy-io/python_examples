# -*- coding: utf-8 -*-
import time
import random

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image


class SVCR:
    def __init__(self, driver):
        self.driver = driver
        self.get_full_img = True

    def run(self):
        # 1. click button to start verify
        self.click_start_btn()

        # 2. according to the type verify
        return self.judge_and_auth()

    def judge_and_auth(self):
        if True:
            return self.auth_slide()
        else:
            pass

    def auth_slide(self):

        def get_distance(img1, img2):
            threshold = 60
            start_x = 57

            for i in range(start_x, img1.size[0]):
                for j in range(img1.size[1]):
                    rgb1 = img1.load()[i, j]
                    rgb2 = img2.load()[i, j]
                    res1 = abs(rgb1[0] - rgb2[0])
                    res2 = abs(rgb1[1] - rgb2[1])
                    res3 = abs(rgb1[2] - rgb2[2])
                    print(res1, res2, res3)
                    if not (res1 < threshold and res2 < threshold and res3 < threshold):
                        return i - 7

        def get_tracks(distance):
            '''
            '''
            v = 0
            current = 0
            t = 0.2
            tracks = []

            # 正向滑动
            while current < distance + 10:
                if current < distance * 3 / 5:
                    a = 2
                else:
                    a = -3
                s = v * t + 0.5 * a * (t**2)
                current += s
                tracks.append(round(s))
                v = v + a * t

            # 往回滑动
            current = 0
            while current < 13:
                if current < distance * 3 / 5:
                    a = 2
                else:
                    a = -3
                s = v * t + 0.5 * a * (t**2)
                current += s
                tracks.append(-round(s))
                v = v + a * t

            # 最后修正
            print(tracks)
            tracks.extend([2, 2, -3, 2])
            print(tracks)
            return tracks

        # 1.截取完整图片
        if self.get_full_img:
            time.sleep(2)
            img_before = self.get_img()
        else:
            img_before = self._img_before

        # 2.点击滑动按钮, 出现缺口图片
        slider_btn = self.driver.find_element_by_class_name('geetest_slider_button')
        slider_btn.click()

        # 3.截取缺口图片
        time.sleep(2)
        img_after = self.get_img()

        # 4.生成移动轨迹
        tracks = get_tracks(get_distance(img_before, img_after))

        # 5.模拟滑动
        slider_btn = self.driver.find_element_by_class_name('geetest_slider_button')
        ActionChains(self.driver).click_and_hold(slider_btn).perform()
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        # 6.释放鼠标
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

        # 7.验证是否成功
        time.sleep(2)
        div_tag = self.driver.find_element_by_class_name('geetest_fullpage_click')
        if 'display: block' in div_tag.get_attribute('style'):
            self.get_full_img = False
            setattr(self, '_img_before', img_before)
            return self.auth_slide()
        else:
            time.sleep(1000)
            return True

    def click_start_btn(self, search_style='CLASS_NAME', search_content='geetest_wait'):
        btn = getattr(self.driver, 'find_element')(getattr(By, search_style), search_content)
        btn.click()

    def get_img(self):
        div_tag = self.driver.find_element_by_class_name('geetest_slicebg')

        img_pt = div_tag.location
        img_size = div_tag.size
        print('img_pt: ', img_pt)
        print('img_size: ', img_size)
        img_box = (img_pt['x'], img_pt['y'], img_pt['x'] + img_size['width'], img_pt['y'] + img_size['height'])

        self.driver.save_screenshot('snap.png')

        img = Image.open('snap.png')
        return img.crop(img_box)


def main():
    driver = webdriver.Chrome()
    driver.get('https://account.geetest.com/login')
    driver.implicitly_wait(3)

    _auth = SVCR(driver)
    _auth.run()


if __name__ == '__main__':
    main()
