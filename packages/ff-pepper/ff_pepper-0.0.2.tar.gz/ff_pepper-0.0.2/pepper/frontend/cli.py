import argparse
import os
import sys

import yaml

import pepper.simple_logger as log
from pepper.config import Router, Manager, InvalidConfigurationError, InvalidArgumentError, sanitize_node_id
from pepper.frontend.core import Pepper, PepperConfig
from pepper.remote_data import FreifunkAPI


class PepperCLI:
    def __init__(self):
        PepperConfig.init()
        self.commands = {
            "apply-all": self.apply_all,
            "apply-node": self.apply_node,
            "apply-group": self.apply_group,
            "apply-hostname": self.apply_hostname,
            "apply-local": self.apply_local,
            "edit": self.edit,
            "init": self.init_dir,
            "setup": self.setup,
            "update": self.update,
            'validate': self.validate_config
        }
        parser = argparse.ArgumentParser(
            description='Configuration tool for Gluon nodes',
            usage='''pepper <command> [<args>]

        The most commonly used pepper commands are:
           apply-all     Apply settings for all nodes
           apply-group   Apply settings for given group
           apply-local   Apply settings for node in config-mode
        ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if args.command not in self.commands:
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)
        self.commands[args.command]()

    def apply_all(self):
        self.pepper = Pepper()
        nodes = self.pepper.config_manager.get_nodes()
        self.pepper.configure_nodes(nodes)

    def apply_group(self):
        self.pepper = Pepper()
        group = sys.argv[2:]
        nodes = self.pepper.config_manager.get_nodes(group=group)
        self.pepper.configure_nodes(nodes)

    def apply_hostname(self):
        self.pepper = Pepper()
        hostname = sys.argv[2:]
        nodes = self.pepper.config_manager.get_nodes(hostname=hostname)
        self.pepper.configure_nodes(nodes)

    def apply_node(self):
        self.pepper = Pepper()
        node = sys.argv[2:]
        nodes = self.pepper.config_manager.get_nodes(node_id=node)
        self.pepper.configure_nodes(nodes)

    def apply_local(self):
        self.pepper = Pepper()
        self.pepper.configure_local(self.pepper.config_manager.get_nodes())

    def init_dir(self):
        Manager.init_directory(os.getcwd())
        sys.exit()

    def edit(self):
        self.pepper = Pepper()
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        parser.add_argument("--hostname", help="Configure a node by its hostname", action="store_true")
        args = parser.parse_known_args(sys.argv[2:])[0]
        w = Wizard(self.pepper.config_manager)
        config = PepperConfig.load_config()
        if args.hostname and 'homeCommunity' in config:
            api = FreifunkAPI(cache_path=PepperConfig.CONFIG_DIR + os.sep, use_cache=True)
            community = api.get_community(config['homeCommunity'])
            while True:
                searchstring = input("Enter Hostname to configure: ")
                nodes = [x for x in community.nodes if searchstring in x['hostname']]
                node_amount = len(nodes)
                if node_amount == 1:
                    log.ok("Configuring {}".format(nodes[0]['node_id']))
                    router = Pepper.router_from_map(nodes[0])
                    w.start_wizard(router_config=router)
                    break
                elif node_amount == 0:
                    log.error("No node found containing '{}'".format(searchstring))
                else:
                    max_full_hostnames = 3
                    msg_string = ", ".join(map(lambda x: x['hostname'], nodes[:max_full_hostnames]))
                    if (len(nodes) > max_full_hostnames):
                        msg_string = msg_string + " and {} more".format(len(nodes) - max_full_hostnames)
                    log.warn("More than one node containing '{}': {}".format(searchstring, msg_string))

        else:
            w.start_wizard()

    def setup(self):
        log.ok('*** Updating data from Freifunk API')
        api = FreifunkAPI(cache_path=PepperConfig.CONFIG_DIR + os.sep, use_cache=False)
        api.update()
        for community in api.api_data:
            print(community)

        while True:
            selected_community = input('Please enter your Freifunk community: ').lower()

            possible_communities = []
            for community in api.api_data:
                if selected_community in community:
                    possible_communities.append(community)

            if len(possible_communities) is 1:
                config = PepperConfig.load_config()
                config['homeCommunity'] = possible_communities[0]
                PepperConfig.save_config(config)
                self.update()
                return True
            elif len(possible_communities) > 1:
                log.info('*** More than one Community containing {input_str}: {communities}'
                         .format(input_str=selected_community, communities=', '.join(possible_communities)))
            elif len(possible_communities) < 1:
                log.info('*** No Community containing {input_str}'
                         .format(input_str=selected_community))

    def update(self):
        api = FreifunkAPI(cache_path=PepperConfig.CONFIG_DIR + os.sep, use_cache=True)
        config = PepperConfig.load_config()
        log.ok('*** Updating community {}'.format(config['homeCommunity']))
        api.update_community(config['homeCommunity'])
        community = api.get_community(config['homeCommunity'])
        node_count = len(community.nodes)
        log.ok('*** Updated community ({} nodes)'.format(node_count))
        if len(community.prefixes) == 1:
            community.primary_prefix = community.prefixes[0]
        elif len(community.prefixes) > 1:
            i = 0
            for prefix in community.prefixes:
                print('{}) {}'.format(str(i), prefix))
                i += 1
            while True:
                try:
                    selected_idx = int(input('Please enter your preferred prefix when connecting.'))
                    if selected_idx < len(community.prefixes):
                        community.primary_prefix = community.prefixes[selected_idx]
                        api.save_community(community)
                        return
                except TypeError as t:
                    pass

    def validate_config(self):
        self.pepper = Pepper()
        exit_code = 0
        for node in self.pepper.config_manager.nodes:
            try:
                self.pepper.config_manager.validate_node_config(node)
                log.ok('*** Valid: {}'.format(node))
            except (InvalidConfigurationError, InvalidArgumentError) as e:
                log.error('*** Invalid: {}'.format(node))
                log.error(str(e))
                exit_code = 1
        sys.exit(exit_code)

class Wizard:
    def __init__(self, manager):
        self.manager = manager

    def set_param(self, msg, obj, param, default=None, empty_allowed=False, type=None):
        if getattr(obj, param) is not None:
            msg = msg + " [{}]:".format(getattr(obj, param))
            empty_allowed = True
        else:
            msg = msg + ':'
        while True:
            try:
                input_val = input(msg)
                if empty_allowed is False and len(input_val) == 0:
                    log.error("Input is empty. Please try again.")
                elif empty_allowed is True and len(input_val) == 0:
                    if default is not None:
                        setattr(obj, param, input_val)
                    break
                else:
                    if type is bool:
                        input_val = self.parsebool(input_val)
                        if input_val is None:
                            continue
                    if type is int and input_val.isdigit():
                        input_val = int(input_val)
                    setattr(obj, param, input_val)
                    break

            except InvalidConfigurationError as e:
                log.error(str(e))
            except InvalidArgumentError as e:
                log.error(str(e))

    def parsebool(self, input):
        if input.strip().lower() in ['1', 'true', 'y', 'yes']:
            return True
        elif input.strip().lower() in ['0', 'false', 'n', 'no']:
            return False
        else:
            return None

    def save_node(self, router_config, path):
        output_data = {}
        target_dir = os.path.join(path + os.sep + 'nodes')

        if self.manager.get_node(router_config.nodeid) is not None:
            save_location = self.manager.node_location[router_config.nodeid]
            with open(save_location, "r") as file:
                output_data = yaml.load(file.read())
        else:
            save_location = target_dir + os.sep + router_config.config.hostname + ".yaml"

        output_data[router_config.nodeid] = router_config.to_dict()

        with open(save_location, "w+") as file:
            file.write(yaml.dump(output_data))
            file.close()

    def list_groups(self):
        for group in self.manager.groups:
            print(" - " + group)

    def get_group_name(self, group_name):
        found_groups = [group for group in self.manager.groups.keys() if group.startswith(group_name)]
        if len(found_groups) is 1:
            return group_name, found_groups[0]
        return group_name, None

    def start_wizard(self, router_config=None):
        if router_config is None:
            router_config = Router()
        self.set_param("The nodes primary MAC/Node_ID", router_config, 'nodeid')
        if self.manager.get_node(sanitize_node_id(router_config.nodeid)) is not None:
            router_config = self.manager.get_node(sanitize_node_id(router_config.nodeid), merge=False)
            log.info("Node {} already exists  - Editing".format(router_config.nodeid))
        self.list_groups()
        while True:
            typed, group_name = self.get_group_name(
                input("Add Group [{}]: ".format(", ".join(router_config.member_of))))
            if len(typed.strip()) is 0:
                break
            if group_name is not None and group_name not in router_config.member_of:
                memberof = router_config.member_of
                memberof.append(group_name)
                router_config.member_of = memberof
                print("Group " + group_name + " added!")
            if len(router_config.member_of) == len(self.manager.groups):
                break
        self.set_param("The nodes hostname", router_config.config, 'hostname')
        self.set_param("Ignore Router", router_config, 'ignore', type=bool)
        self.set_param("Activate Mesh-LAN".format(router_config.config.mesh_lan),
                       router_config.config, 'mesh_lan', type=bool, empty_allowed=True)
        self.set_param("Activate Mesh-WAN".format(router_config.config.mesh_wan),
                       router_config.config, 'mesh_wan', type=bool, empty_allowed=True)
        # Prefix
        if self.parsebool(input("Configure 5GHz WiFi?")):
            self.set_param("Enable Client WiFi", router_config.config.wireless.band_5, 'client',
                           type=bool, empty_allowed=True)
            self.set_param("Enable Mesh WiFi", router_config.config.wireless.band_5, 'mesh',
                           type=bool, empty_allowed=True)
            self.set_param("Set WiFi channel", router_config.config.wireless.band_5, 'channel',
                           type=int, empty_allowed=True)

        if self.parsebool(input("Configure 2.4GHz WiFi?")):
            self.set_param("Enable Client WiFi", router_config.config.wireless.band_24, 'client',
                           type=bool, empty_allowed=True)
            self.set_param("Enable Mesh WiFi", router_config.config.wireless.band_24, 'mesh',
                           type=bool, empty_allowed=True)
            self.set_param("Set WiFi channel", router_config.config.wireless.band_24, 'channel',
                           type=int, empty_allowed=True)
        self.save_node(router_config, self.manager.working_dir)
