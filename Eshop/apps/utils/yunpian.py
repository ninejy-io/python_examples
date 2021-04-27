# import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunppian.com/v2/sms/single_send"

    def send_sms(self, code, mobile):
        data = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "Your verify code is {}, please keep your code safe.".format(code)
        }
        # res = requests.post(self.single_send_url, data=data)
        # return res.json()
        return {"code": 0, "msg": "ok"}
