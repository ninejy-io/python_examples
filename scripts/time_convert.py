import time


timestamp = time.time()
datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
print(timestamp)    # 1577028742.451523
print(datetime)     # 2019-12-22 23:32:22

# 1577028742.451523 -> 2019-12-22 23:32:22
ts = 1577028742.451523
_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
print(_dt)          # 2019-12-22 23:32:22

# 2019-12-22 23:32:22 -> 1577028742
dt = '2019-12-22 23:32:22'
_ts = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
print(_ts)          # 1577028742.0

# 2019-12-22 23:32:22 -> 20191222233222
dt2 = time.strftime('%Y%m%d%H%M%S', time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
print(dt2)          # 20191222233222
