from collections import namedtuple
from ansible import constants
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.host import Host, Group

host_list_file = "/etc/ansible/hosts"


class MyInventory:

    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=[host_list_file])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, group_name, group_vars=None):
        self.inventory.add_group(group_name)
        my_group = Group(name=group_name)

        if group_vars is not None:
            for k, v in group_vars.items():
                my_group.set_variable(k, v)

        for host in hosts:
            hostname = host.get("hostname")
            hostip = host.get("ip", hostname)
            hostport = host.get("port", 22)
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key", "~/.ssh/id_rsa")
            my_host = Host(name=hostname, port=hostport)

            self.variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_host", value=hostip)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_pass', value=password)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_port', value=hostport)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_user', value=username)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_private_key_file', value=ssh_key)

            for key, value in host.items():
                if key not in ["hostname", "port", "username", "password"]:
                    self.variable_manager.set_host_variable(host=my_host, varname=key, value=value)

            self.inventory.add_host(host=hostname, group=group_name, port=hostport)

    def dynamic_inventory(self):
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, "default_group")
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


class ModelResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_unreachable = {}
        self.host_ok = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class PlaybookResultsCollector(CallbackBase):

    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(PlaybookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_failed = {}
        self.task_skipped = {}
        self.task_unreachable = {}
        self.task_status = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                    "ok": t["ok"],
                    "changed": t["changed"],
                    "unreachable": t["unreachable"],
                    "skipped": t["skipped"],
                    "failed": t["failures"]
                }


class AnsibleRunner(object):

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        Options = namedtuple('Options',
                            ['connection',
                             'module_path',
                             'forks',
                             'timeout',
                             'remote_user',
                             'ask_pass',
                             'private_key_file',
                             'ssh_common_args',
                             'ssh_extra_args',
                             'sftp_extra_args',
                             'scp_extra_args',
                             'become',
                             'become_method',
                             'become_user',
                             'ask_value_pass',
                             'verbosity',
                             'check',
                             'listhosts',
                             'listtasks',
                             'listtags',
                             'syntax',
                             'diff'])
        self.loader = DataLoader()
        self.options = Options(connection='smart',
                               module_path=None,
                               forks=100,
                               timeout=10,
                               remote_user='root',
                               ask_pass=False,
                               private_key_file=None,
                               ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None,
                               scp_extra_args=None,
                               become=None,
                               become_method=None,
                               become_user='root',
                               ask_value_pass=False,
                               verbosity=None,
                               check=False,
                               listhosts=False,
                               listtasks=False,
                               listtags=False,
                               syntax=False,
                               diff=True)
        self.passwords = dict(sshpass=None, becomepass=None)
        my_inventory = MyInventory(self.resource, self.loader, self.variable_manager)
        self.inventory = my_inventory.inventory
        self.variable_manager = my_inventory.variable_manager

    def run_model(self, host_list, module_name, module_args):
        play_source = dict(
                name="Ansible Play",
                hosts=host_list,
                gather_facts='no',
                tasks=[dict(action=dict(module=module_name, args=module_args))]
        )

        play = Play().load(play_source, loader=self.loader, variable_manager=self.variable_manager)
        tqm = None
        self.callback = ModelResultsCollector()
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
                    stdout_callback = "minimal",
            )
            tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False
            tqm.run(play)
        except Exception as e:
            print("{}".format(e))
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbook_path, extra_vars=None):
        try:
            self.callback = PlaybookResultsCollector()
            if extra_vars:self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(playbooks=[playbook_path],
                                        inventory=self.inventory,
                                        variable_manager=self.variable_manager,
                                        loader=self.loader,
                                        options=self.options,
                                        passwords=self.passwords,
                                    )
            executor._tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False
            executor.run()
        except Exception as e:
            print("{}".format(e))
            return False

    def get_model_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['success'][hostvisiable] = result._result

        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['failed'][hostvisiable] = result._result

        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['unreachable'][hostvisiable]= result._result

        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped':{}, 'failed':{}, 'ok':{},"status":{},'unreachable':{},"changed":{}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return self.results_raw


if __name__ == '__main__':
    resource =  {
        "all": {
            "hosts": [
                {"hostname":"192.168.1.202", "ip": "192.168.1.202", "port": "22"},
                {"hostname":"192.168.1.203", "ip": "192.168.1.203", "port": "22"}                          ],
            "vars": {
                "var1":"ansible",
                "var2":"saltstack"
            }
        }
    }
    # resource = [{"hostname": "127.0.0.1"}, {"hostname": "192.168.1.101"}]
    rbt = AnsibleRunner(resource)
    # Ansible Adhoc
    # rbt.run_model(host_list=['127.0.0.1', '172.31.39.251', 'robert'],module_name='shell',module_args="ls /tmp")
    # data = rbt.get_model_result()
    # print(data)
    # Ansible playbook
    rbt.run_playbook(playbook_path='test.yml', extra_vars={"name": "robert","version": "123456"})
    data2 = rbt.get_playbook_result()
    print(data2)
