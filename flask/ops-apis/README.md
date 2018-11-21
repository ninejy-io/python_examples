#### Apis are used to update or check nginx config
- ###### Install and start
```shell
pip install -r requirements.txt
python app.py
```
###### Notice: server accept params only in json format
---
- ###### check nginx config
```shell
url: http://ip:port/checkconfig
method: POST
param:
{
    "server_group_name": "",
    "git_version": ""
}
```
---
- ###### update nginx config
```shell
url: http://ip:port/updateconfig
method: POST
param:
{
    "server_group_name": "",
    "git_version": "",
    "server_nodes": []
}
```