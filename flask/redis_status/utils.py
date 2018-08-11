import os
# from subprocess import Popen, PIPE
from redis_faina import StatCounter


cur_dir = os.path.dirname(os.path.abspath(__file__))
temp_file_name = cur_dir + '/tmp/' + 'monitor_log.txt'
script_name = cur_dir + '/get_data.sh &'


def load_info():
    os.system('/bin/bash %s' % script_name)
    os.system("ps -ef|grep redis-cli|grep -v grep |awk '{print $2}'|xargs kill -9 ")
    try:
        fd = open(temp_file_name, 'r')
        counter = StatCounter()
        counter.process_input(fd)
        result = counter.handle_data()
        fd.close()
    except Exception:
        result = {"msg": "no data"}
    return result
