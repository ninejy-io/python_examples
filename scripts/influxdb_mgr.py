import random
from datetime import datetime

from influxdb import InfluxDBClient


## HTTP
# client = InfluxDBClient(database='mydb')
client = InfluxDBClient(host='192.168.199.24', port=8086, database='mydb')
# client = InfluxDBClient(host='127.0.0.1', port=8086, database='mydb', username='admin', password='123456')
# client = InfluxDBClient.from_dsn('influxdb://username:password@localhost:8086/databasename', timeout=5)

## UDP
# client = InfluxDBClient(host='127.0.0.1', database='mydb', use_udp=True, udp_port=4444)
# client = InfluxDBClient.from_dsn('udp+influxdb://username:password@localhost:8086/databasename', timeout=5, udp_port=159)

## pandas dataframes
# from influxdb import DataFrameClient
# client = DataFrameClient(host='127.0.0.1', port=8086, username='admin', password='123456')

'''
client.write({"points": [
                    {
                        "measurement": "disk_info",
                        "tags": {
                            "host": "server-01",
                            "region": "us-west"
                        },
                        "time": "2018-3-26T19:19:20Z",
                        "fields": {
                            "total_value": 200000000000,
                            "used_value": 30000000
                        }
                    },
                    {
                        "measurement": "disk_info",
                        "tags": {
                            "host": "server-02",
                            "region": "us-west"
                        },
                        "fields": {
                            "total_value": 200000000000,
                            "used_value": 40000000
                        }
                    }
                ]
            })
'''

'''
client.write_points(
    [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2018-3-26T19:20:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]
)
'''

def insert(times=10, nums_per=1000):
    for i in range(times):
        data = []
        for j in range(nums_per):
            data.append(
                {
                    "measurement": "host_load_info",
                    "tags": {
                        "host_ip": "127.0.0.1",
                        "project": "test_project"
                    },
                    "time": datetime.now(),
                    "fields": {
                        "cpu_load": random.randint(1, 4),
                        "mem_used": random.randint(100000000000, 900000000000),
                        "mem_total": 80000000000000000,
                        "disk_used": random.randint(30000000, 60000000),
                        "disk_total": 2000000000000000000
                    }
                }
            )
        print(data)
        client.write_points(data)

s = datetime.now()
insert()
e = datetime.now()
print("Total time is: {}".format(e-s))


# res = client.query('select * from cpu_load_short')
# print("Result: {}".format(res))

# res2 = client.request('write', u'POST', params=None, data=None, expected_response_code=200, headers=None)  # write/query etc.
# print(res2)

## send an UDP packet
# client.send_packet({'packet': 'something'}, protocol=u'json')  # (if protocol is 'json') dict, (if protocol is 'line') string

# client.create_database('mydb2')
# client.switch_database('mydb2')
# dbs = client.get_list_database()
# client.drop_database('mydb2')

# measurements = client.get_list_measurements()
# client.drop_measurement('cpu_load_short')

# client.create_retention_policy('my_retention', '4w', '1', database='mydb', default=False)
# retention_policies = client.get_list_retention_policies()
# client.drop_retention_policy('my_retention')

# client.create_user('username', 'password', admin=False)
# client.switch_user('username', 'password')
# client.set_user_password('username')
# users = client.get_list_users()
# client.drop_user('username')

# client.grant_admin_privileges('username')
# client.revoke_admin_privileges('username')
# client.grant_privilege('read', 'mydb2', 'username')  # read/write/all
# client.revoke_privilege('read', 'mydb2', 'username')

client.close()
