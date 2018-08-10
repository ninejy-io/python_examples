import datetime
import string
import random
import elasticsearch
from elasticsearch.helpers import bulk


es = elasticsearch.Elasticsearch(['127.0.0.1'])
# es = elasticsearch.Elasticsearch(['127.0.0.1'], http_auth=('user', 'password'), port=9200)

_index = "blog_index"
_doc_type = "post"
_index_mapping = {
    _doc_type: {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "num": {"type": "number"},
            "time": "date"
        }
    }
}

if es.indices.exists(index=_index) is not True:
    es.indices.create(index=_index, body=_index_mapping)


def insert(nums=10000):
    for i in range(nums):
        data = {
            "title": ''.join(random.sample(string.ascii_letters, 12)),
            "author": ''.join(random.sample(string.ascii_letters, 6)),
            "num": int(''.join(random.sample(string.digits, 6))),
            "time": datetime.datetime.now()
        }
        es.index(index=_index, doc_type=_doc_type, body=data)

# s = datetime.datetime.now()
# insert()
# e = datetime.datetime.now()
# print("total time is: {}".format(e-s))


def insert_many(times=10, nums_per=10000):
    for i in range(times):
        data = []
        for j in range(nums_per):
            data.append({
                "_index": _index,
                "_type": _doc_type,
                "_source": {
                        "title": ''.join(random.sample(string.ascii_letters, 12)),
                        "author": ''.join(random.sample(string.ascii_letters, 6)),
                        "num": int(''.join(random.sample(string.digits, 6))),
                        "time": datetime.datetime.now()
                    }
                })
        print(len(data))
        bulk(es, data, index=_index)

'''
s2 = datetime.datetime.now()
insert_many()
e2 = datetime.datetime.now()
print("Total time is: {}".format(e2-s2))
print("Total docs is: {}".format(es.count()['count']))
'''


# print("Search all...")
# _query = {
#     "query": {
#         "match_all": {}
#     }
# }

# searched = es.search(index=_index, doc_type=_doc_type, body=_query, size=100)
# print(searched)

# for hit in searched["hits"]["hits"]:
#     print(hit["_source"])


# print("Author contains 'Jack'...")
# _query_author = {
#     "query": {
#         "match": {
#             "Author": "Jack"
#         }
#     }
# }

# _res = es.search(index=_index, doc_type=_doc_type, body=_query_author)
# print(_res)
