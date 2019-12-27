from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch(['192.168.0.13:9200'], sniff_on_start=True)

# create 
# body = {'settings': {}, 'mappings': {}}
# es.indices.create(index='my-index')

# insert data
# es.index(index='my-index', body={'any': 'data01', 'timestamp': datetime.now()}, doc_type='test-type', id=0)

# get data
# data = es.get(index='my-index', id=0) #['_source']
# print(data)

# delete data
# es.delete(index='my-index', id=0)

# batch insert data
# data = [
#     {'index': {}},
#     {'name': 'robert', 'age': 20, 'sex': 'male', 'edu': 'University'},
#     {'index': {}},
#     {'name': 'jack', 'age': 15, 'sex': 'female', 'edu': 'High'}
# ]
# es.bulk(body=data, doc_type='test-type', index='my-index')

# search all data
# data = es.search(index='my-index')
# data = es.search(index='my-index', body={'query': {'match_all': {}}})
# print(data)

# search by term/terms
# es.search(index='my-index', body={'query': {'term': {'name': 'python'}}})  # name='python'
# es.search(index='my-index', body={'query': {'terms': {'name': ['python', 'golang']}}})  # name='python' or name='golang'

# search by match/multi_match
# es.search(index='my-index', body={'query': {'match': {'name': 'python'}}})  # name contains 'python'
# es.search(index='my-index', body={'query': {'multi_match': {'query': 'python', 'fields': ['name', 'addr']}}})  # name or addr contains 'python'

# search by ids
# es.search(index='my-index', body={'query': {'ids': {'values': ['1', '2']}}})  # id='1' or id='2'

# search by mutil bool
# body = {
#     "query": {
#         "bool": {
#             "must": [  # must(都满足), should(其中一个满足), must_not(都不满足)
#                 {"term": {"name": "python"}},
#                 {"term": {"age": 18}}
#             ]
#         }
#     }
# }
# es.search(index='my-index', body=body)  # name='python' and age=18

# search slice
# body = {"query": {"match_all": {}}, "from": 2, "size": 4}
# es.search(index='my-index', body=body)  # get 4 pieces data start with the second.

# search range
# body = {"query": {"range": {"age": {"gte": 18, "lte": 30}}}}
# es.search(index='my-index', body=body)  # get data which 18 <= age <= 30

# search prefix
# body = {"query": {"prefix": {"name": "p"}}}
# es.search(index='my-index', body=body)  # get data which name prefix is 'p'

# search wildcard
# body = {"query": {"wildcard": {"name": "*id"}}}
# es.search(index='my-index', body=body)  # get data which name end with 'id'

# search sort
# body = {"query": {"match_all": {}, "sort": {"age": {"order": "asc"}}}}
# es.search(index='my-index', body=body)  # order by age asc(up)/ desc(down)

# search filter_path
# ###es.search(index='my-index', filter_path=['hits.hits._id'])

# count result
# es.count(doc_type='test-type', index='my-index', body={"query": {"match_all": {}}})

# get min value
# body = {
#     "query": {"match_all": {}},
#     "aggs": {
#         "min_age": {  # alias of min value
#             "min": {"field": "age"}
#         }
#     }
# }
# es.search(index='my-index', body=body)  # get the min age

# get max value
# body = {
#     "query": {"match_all": {}},
#     "aggs": {
#         "max_age": {
#             "max": {"field": "age"}
#         }
#     }
# }
# es.search(index='my-index', body=body)  # get the max age

# get sum
# body = {
#     "query": {"match_all": {}},
#     "aggs": {
#         "sum_age": {
#             "sum": {"field": "age"}
#         }
#     }
# }
# es.search(index='my-index', body=body)  # get age sum

# get avg
body = {
    "query": {"match_all": {}},
    "aggs": {
        "avg_age": {
            "avg": {"field": "age"}
        }
    }
}
es.search(index='my-index', body=body)  # get age avg

query = {'query': {'match': {'sex': 'female'}}}
es.update_by_query('my-index', body=query)

# query = {'query': {'range': {'age': {'lt': 18}}}}
# es.delete_by_query('my-index', body=query)
