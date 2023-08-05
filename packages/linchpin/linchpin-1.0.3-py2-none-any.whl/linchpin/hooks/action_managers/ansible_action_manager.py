import os
import yaml
import json

from cerberus import Validator
from collections import namedtuple

from ansible import utils
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor

from linchpin.exceptions import HookError
from linchpin.hooks.action_managers.action_manager import ActionManager


class AnsibleActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        """
        AnsibleActionManager constructor
        :param name: Name of Action Manager , ( ie., ansible)
        :param action_data: dictionary of action_block
        consists of set of actions
        example:
        - name: nameofthehook
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "test_var": "postdowntask"}
        :param target_data: Target specific data defined in PinFile
        :param kwargs: anyother keyword args passed as metadata
        """

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get("context", True)
        self.kwargs = kwargs


    def validate(self):

        """
        Validates the action_block based on the cerberus schema
        example:: ansible_action_block::::
        - name: build_openshift_cluster
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "testvar": "world"}
        """

        schema = {
            'name': {'type': 'string', 'required': True},
            'type': {'type': 'string', 'allowed': ['ansible']},
            'path': {'type': 'string', 'required': False},
            'context': {'type': 'boolean', 'required': False},
            'actions': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'playbook': {'type': 'string', 'required': True},
                        'vars': {'type': 'string', 'required': False},
                        'extra_vars': {'type': 'dict', 'required': False}
                    }
                },
                'required': True
            }
        }

        v = Validator(schema)
        status = v.validate(self.action_data)

        if not status:
            raise HookError("Invalid syntax: {0}".format(+str((v.errors))))
        else:
            return status


    def load(self):

        """
        Loads the ansible specific managers and loaders
        """

        self.loader = DataLoader()
        self.variable_manager = VariableManager()
        self.passwords = {}

        if 'inventory_file' in self.target_data and self.context:
            self.inventory = (
                Inventory(loader=self.loader,
                          variable_manager=self.variable_manager,
                          host_list=self.target_data["inventory_file"]))
        else:
            self.inventory = Inventory(loader=self.loader,
                                       variable_manager=self.variable_manager,
                                       host_list=["localhost"])

        Options = namedtuple('Options', ['listtags',
                                         'listtasks',
                                         'listhosts',
                                         'syntax',
                                         'connection',
                                         'module_path',
                                         'forks',
                                         'remote_user',
                                         'private_key_file',
                                         'ssh_common_args',
                                         'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args',
                                         'become',
                                         'become_method',
                                         'become_user',
                                         'verbosity',
                                         'check'])

        utils.VERBOSITY = 4

        self.options = Options(listtags=False,
                               listtasks=False,
                               listhosts=False,
                               syntax=False,
                               connection='ssh',
                               module_path="",
                               forks=100,
                               remote_user='root',
                               private_key_file=None,
                               ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None,
                               scp_extra_args=None,
                               become=False,
                               become_method="sudo",
                               become_user='root',
                               verbosity=utils.VERBOSITY,
                               check=False)


    def get_ansible_runner(self, playbook_path, extra_vars):

        """
        Fetches ansible runner based on playbook_path and extra_vars
        :param playbook_path: path to playbook
        :param extra_vars: variables to be passed
        """

        self.variable_manager.extra_vars = extra_vars

        # verbosity through api doesn't work
        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords=self.passwords)

        return pbex


    def get_ctx_params(self):

        """
        Reformats the ansible specific variables
        """

        ctx_params = {}
        ctx_params["resource_file"] = (
            self.target_data.get("resource_file", None))
        ctx_params["layout_file"] = self.target_data.get("layout_file", None)
        ctx_params["inventory_file"] = (
            self.target_data.get("inventory_file", None))

        return ctx_params


    def execute(self):

        """
        Executes the action_block in the PinFile
        """

        self.load()
        extra_vars = {}

        for action in self.action_data["actions"]:
            path = self.action_data["path"]
            playbook = action.get("playbook")

            if not(os.path.isfile(playbook)):
                playbook = "{0}/{1}".format(path, playbook)

            if "vars" in action:
                var_file = "{0}/{1}".format(path, action.get("vars"))
                ext = var_file.split(".")[-1]
                extra_vars = open(var_file, "r").read()

                if ("yaml" in ext) or ("yml" in ext):
                    extra_vars = yaml.load(extra_vars)
                else:
                    extra_vars = json.loads(extra_vars)

            e_vars = action.get("extra_vars", {})
            extra_vars.update(e_vars)

            if self.context:
                extra_vars.update(self.get_ctx_params())

            pbex = self.get_ansible_runner(playbook, extra_vars)
            # if desired, results can be collected with results = pbex.run()
            pbex.run()
