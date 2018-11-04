from flask import current_app
from .ansible_api import AnsibleRunner
from config import BASE_DIR, NODE_GROUP_NAME, GIT_ADDRESS_PREFIX, CHECK_RESOURCE
import logging


def check_nginx_config(**kwargs):
    '''
    json_data = {
        "server_group_name": "uledns",
        "git_version": "1.0.1"
    }
    '''
    logging.info("check kwargs: " + str(kwargs))
    server_group_name = kwargs.get('server_group_name')
    git_version = kwargs.get('git_version')

    if server_group_name and git_version:
        CHECK_RESOURCE["check_nodes"]["vars"] = {"git_address": GIT_ADDRESS_PREFIX.format(server_group_name), "git_version": git_version}
        rbt = AnsibleRunner(CHECK_RESOURCE)
        rbt.run_playbook(BASE_DIR + '/playbook/check_nginx_config.yaml',
                        extra_vars={"git_address": GIT_ADDRESS_PREFIX.format(server_group_name), "git_version": git_version})
        result = rbt.get_playbook_result()
        logging.info(str(result["status"]))
        if result['failed'] or result['unreachable']:
            logging.error(str(result["failed"]) + str(result["unreachable"]))
            return False
        return True
    return False


def update_nginx_config(**kwargs):
    '''
    json_data = {
        "server_group_name": "uledns",
        "server_nodes": ["192.168.1.202", "192.168.1.203"],
        "git_version": "1.0.1"
    }
    '''
    logging.info("update kwargs: " + str(kwargs))
    server_group_name = kwargs.get('server_group_name')
    server_nodes = kwargs.get('server_nodes')
    git_version = kwargs.get('git_version')

    if server_group_name and server_nodes and git_version:
        for server in server_nodes:
            resource = {}
            resource[NODE_GROUP_NAME] = {
                "hosts": [{"hostname": server, "ip": server}],
                "vars": {"git_address": GIT_ADDRESS_PREFIX.format(server_group_name), "git_version": git_version}
            }
            rbt = AnsibleRunner(resource)
            rbt.run_playbook(BASE_DIR + '/playbook/update_nginx_config.yaml',
                            extra_vars={"git_address": GIT_ADDRESS_PREFIX.format(server_group_name), "git_version": git_version})
            result = rbt.get_playbook_result()
            logging.info(str(result["status"]))
            if result['failed'] or result['unreachable']:
                logging.error(str(result["failed"]) + str(result["unreachable"]))
                return False
        return True
    return False
