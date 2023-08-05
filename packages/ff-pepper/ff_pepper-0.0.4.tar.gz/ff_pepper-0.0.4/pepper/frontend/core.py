import os

import yaml

import pepper.simple_logger as log
from pepper import connection as r
from pepper.config import InvalidConfigurationError, Router, Manager
from pepper.gluon import GluonWeb


class PepperConfig:
    CONFIG_DIR = os.path.expanduser('~') + os.sep + '.pepper'
    PEPPER_CONFIGFILE_PATH = CONFIG_DIR + os.sep + 'config.yaml'

    @staticmethod
    def init(dir=CONFIG_DIR):
        if not os.path.isdir(dir):
            os.makedirs(dir)
        if not os.path.exists(PepperConfig.PEPPER_CONFIGFILE_PATH):
            open(PepperConfig.PEPPER_CONFIGFILE_PATH, 'a').close()

    @staticmethod
    def read_data(path):
        with open(path, 'r') as file:
            data = yaml.load(file.read())
            return data if data is not None else {}

    @staticmethod
    def write_data(path, data):
        with open(path, 'w+') as file:
            file.write(yaml.dump(data, allow_unicode=True))

    @staticmethod
    def load_config():
        return PepperConfig.read_data(PepperConfig.PEPPER_CONFIGFILE_PATH)

    @staticmethod
    def save_config(data):
        PepperConfig.write_data(PepperConfig.PEPPER_CONFIGFILE_PATH, data)


class Pepper:
    def __init__(self, config_manager=True):
        if config_manager:
            self.config_manager = Manager(os.getcwd())

    @staticmethod
    def configure_remote(node):
        ip6 = node.get_ip6()
        log.info("*** Connecting to", ip6)
        router = r.RouterConnection(ip6)
        try:
            router.connect()
        except Exception as e:
            return
        node.configure(router)
        router.commit()
        router.disconnect()

    @staticmethod
    def configure_local(nodes):
        GluonWeb.store_ssh_keys(nodes)
        router = r.RouterConnection("192.168.1.1")
        router.connect()
        node = nodes[router.get_primary_mac().replace(':', '')]
        node.configure(router)
        router.set_configured(1)
        router.commit()
        router.reboot()

    @staticmethod
    def router_from_map(map):
        router = Router()
        router.nodeid = map['node_id']
        router.config.hostname = map['hostname']
        return router

    def configure_nodes(self, nodes):
        for node in nodes:
            if nodes[node].ignore == True:
                log.warn("\n*** Ignoring " + node)
                continue
            log.ok("*** Configuring " + node)
            try:
                self.config_manager.validate_node_config(node)
                self.configure_remote(nodes[node])
            except InvalidConfigurationError as e:
                log.error("*** Invalid Configuration for node {}: {}".format(node, str(e)))
