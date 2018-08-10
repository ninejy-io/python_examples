# -*- coding: utf-8 -*-
from collections import namedtuple, deque, OrderedDict, defaultdict, Counter

# namedtuple
'''
point = namedtuple('point', ['x', 'y'])
p = point(1, 2)
print(p.x, p.y)
'''

# deque
'''
q = deque(['a', 'b', 'c'])
q.append('ee')
q.append('ff')
print(q)

q.appendleft('www')
print(q)

q.pop()
q.popleft()
print(q)
'''

# OrderedDict
'''
d = {'z': 'qww', 'x': 'asd', 'y': 'asd', 'name': 'jim'}
print(d.keys())  # key是无序的

od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)

od2 = OrderedDict()
od2['z'] = 1
od2['y'] = 2
od2['x'] = 3
print(od2)  # 按照插入的顺序返回
'''

# defaultdict
'''
values = [11, 22, 33, 44, 55, 66, 77, 88, 99]
my_dict = defaultdict(list)
print(my_dict)
for v in values:
    if v > 66:
        my_dict['k1'].append(v)
    else:
        my_dict['k2'].append(v)
print(my_dict)

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])
'''

# Counter

c = Counter()
c = Counter('asdfasdfefgh')
c = Counter(['a', 'b', 'c'])
c = Counter((1, 2, 3, 4))
c = Counter({'a': 2, 'b': 3})
c = Counter(a=2, b=3)

d = Counter('abcde')
c.update(d)    # 增加
c.subtract(d)  # 减少
del c['a']     # 删除

e = Counter(a=3, b=2, c=0)
print(list(e.elements()))

c = Counter('abcdeabcdabcaba')
print(c)
print(c.most_common(2))
print(c.most_common()[:2:-1])
print(sum(c.values()))
