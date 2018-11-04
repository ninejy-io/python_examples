import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# used by ansible to located nginx server
NODE_GROUP_NAME = "production_nodes"

# git address about your project
GIT_ADDRESS_PREFIX = "https://github.com/jy90/{}.git"

# nginx check node info
CHECK_RESOURCE = {
    "check_nodes": {
        "hosts": [{"hostname": "192.168.152.116", "ip": "192.168.152.116"}],
        "vars": {}
    }
}
