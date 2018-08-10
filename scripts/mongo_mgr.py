from datetime import datetime
import random
import string
import pymongo


client = pymongo.MongoClient('192.168.199.24', 27017)

db = client['my_db']
collection = db['my_collection']


def insert(nums):
    for i in range(nums):
        data = {
            "name": ''.join(random.sample(string.ascii_letters, 12)),
            "author": ''.join(random.sample(string.ascii_letters, 6)),
            "num": int(''.join(random.sample(string.digits, 6))),
            "time": datetime.now(),
        }
        collection.insert(data)


s = datetime.now()
insert(10000)
e = datetime.now()
print("total time is: {}".format(e-s))
# _data = collection.find({'name': 'robert'})
# print(dict(_data))

