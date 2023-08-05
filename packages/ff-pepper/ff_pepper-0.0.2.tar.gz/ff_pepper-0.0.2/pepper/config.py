import copy
import ipaddress
import os
import re
import subprocess
import sys
from enum import Enum

import yaml

import pepper.simple_logger as log
from pepper.connection import WIRELESS_TYPE


def sanitize_node_id(nid):
    return nid.replace(':', '').replace('-', '').strip().lower()


class InvalidConfigurationError(Exception):
    pass


class Manager:
    DIR_SSH = 'ssh'
    DIR_GROUPS = 'groups'
    DIR_NODES = 'nodes'

    def __init__(self, path):
        self.groups = {}
        self.nodes = {}
        self.node_location = {}
        self.ssh_keys = {}

        self.working_dir = path

        self.load_ssh_keys(os.path.join(path + os.sep + Manager.DIR_SSH))
        self.load_groups(os.path.join(path + os.sep + Manager.DIR_GROUPS))
        self.load_nodes(os.path.join(path + os.sep + Manager.DIR_NODES))

    @staticmethod
    def init_directory(path):
        if not os.path.exists(path + os.sep + Manager.DIR_SSH):
            os.makedirs(path + os.sep + Manager.DIR_SSH)
        if not os.path.exists(path + os.sep + Manager.DIR_GROUPS):
            os.makedirs(path + os.sep + Manager.DIR_GROUPS)
        if not os.path.exists(path + os.sep + Manager.DIR_NODES):
            os.makedirs(path + os.sep + Manager.DIR_NODES)

    def load_ssh_keys(self, path):
        available_keys = os.listdir(path)
        for key in available_keys:
            with open(path + '/' + key, 'r') as f:
                p = subprocess.Popen('ssh-keygen -l -f ' + path + '/' + key, shell=True, stdout=open(os.devnull, 'w'))
                p.communicate()
                if p.returncode is not 0:
                    sys.exit("Keyfile " + path + '/' + key + ' is not valid.')
                self.ssh_keys[key] = f.readline().replace('\n', '')
                f.close()

    def load_nodes(self, path):
        found_node_names = []
        for filename in os.listdir(path):
            filepath = path + '/' + filename
            with open(filepath, 'r') as f:
                file_content = f.read()

                node_names = re.findall('\'([0-9a-f]{12}|(?:[0-9a-f]{2}:){5}[0-9a-f]{2})\'', file_content)
                found_node_names += map((lambda x: sanitize_node_id(x)), node_names)

                if len(set(found_node_names)) != len(found_node_names):
                    raise Exception('Multiple nodes with same name while reading ' + filename)

                nodes = yaml.load(file_content)
                for node in nodes:
                    self.nodes[node] = nodes[node]
                    self.node_location[node] = filepath

    def load_groups(self, path):
        for filename in os.listdir(path):
            group = filename.replace('.yaml', '').replace('.yml', '')
            with open(path + '/' + filename, 'r') as f:
                file_content = yaml.load(f.read())
                self.groups[group] = file_content

    def get_group(self, group_name):
        group = self.groups[group_name]
        if 'member-of' in group:
            for group_name in group['member-of'][::-1]:
                group = self.merge(group, self.groups[group_name])
        return Group(group_name, group)

    @staticmethod
    def merge(child, parent):
        out = copy.deepcopy(child)
        for key in parent:
            if key not in child:
                out[key] = parent[key]
            elif type(parent[key]) != type(child[key]):
                raise InvalidConfigurationError("Parent config object {} is not the same as the Childs!".format(key))
            elif type(child[key]) is dict:
                out[key] = Manager.merge(child[key], parent[key])
            elif type(child[key]) is list:
                for element in parent[key]:
                    if element not in out[key]:
                        out[key].append(parent[key])

        return out

    @staticmethod
    def replace_ssh_keys(root_obj, ssh_keys):
        # replace ssh key names with real ssh keys
        if RouterConfig.KEY_SSH in root_obj["config"]:
            keys = []
            for key in root_obj['config'][RouterConfig.KEY_SSH]:
                keys.append(ssh_keys[key])
            root_obj['config'][RouterConfig.KEY_SSH] = keys
        return root_obj

    def get_node(self, node_id, merge=True):
        if node_id not in self.nodes:
            return None
        node = copy.deepcopy(self.nodes[node_id])
        if merge and 'member-of' in node:
            for group_name in node['member-of'][::-1]:
                node = self.merge(node, self.get_group(group_name).to_dict())
        return Router(node_id, self.replace_ssh_keys(node, self.ssh_keys))

    def get_nodes(self, group=[], node_id=[], hostname=[]):
        nodes = {}
        groups = ([group] if isinstance(group, str) else group)
        node_ids = ([sanitize_node_id(node_id)] if isinstance(node_id, str) else
                    [sanitize_node_id(n) for n in node_id])
        hostnames = ([hostname] if isinstance(hostname, str) else hostname)
        for node in self.nodes:
            node_obj = self.get_node(node)
            if (not group and not node_id and not hostname) or \
                    (groups and [group for group in groups if group in node_obj.member_of]) or \
                    (node_ids and node in node_ids) or \
                    (hostnames and node_obj.config.hostname in hostnames):
                nodes[node] = node_obj
        return nodes

    def filter_group_members(self, *groups):
        nodes = {}
        for node_id in self.nodes:
            for group in groups:
                if group in self.nodes[node_id]['member-of']:
                    nodes[node_id] = self.nodes[node_id]
                    break
        self.nodes = nodes

    def filter_nodes(self, *nodes):
        output_nodes = {}
        for node_id in self.nodes:
            for node in nodes[0]:
                if sanitize_node_id(node_id) == sanitize_node_id(node):
                    output_nodes[node_id] = self.nodes[node_id]
        self.nodes = output_nodes

    def validate_node_config(self, node_id):
        allowed_keys = [getattr(RouterConfig, attr) for attr in dir(RouterConfig) if attr.startswith('KEY_')]
        node = self.get_node(node_id)

        def check_keys(config):
            for key in config.keys():
                if key not in allowed_keys:
                    raise Exception("Invalid key found for node " + node.node_id + ": " + key)

        check_keys(node.config.plain_config)

        # Check for simultaneous activated vpn and mesh_wan
        if node.config.fastd_active and node.config.mesh_wan:
            raise InvalidConfigurationError("Can't enable mesh_vpn and mesh_wan at the same time")

        # Check for simultaneous activated private-wifi and mesh_wan
        if node.config.wireless.private_wifi.enabled and node.config.mesh_wan:
            raise InvalidConfigurationError("Can't enable mesh_vpn and mesh_wan at the same time")

        # Check for to short wifi password
        if node.config.wireless.private_wifi.password != None and len(
                node.config.wireless.private_wifi.password) < 8:
            raise InvalidConfigurationError("Private-WiFi password must be at least 8 characters long")

    def validate_config(self):
        nodes = self.get_nodes()

        for nodeid in nodes:
            self.validate_node_config(nodeid)


class InvalidArgumentError(Exception):
    class Errors(Enum):
        MIN_LENGTH = 1
        MAX_LENGTH = 2
        EXACT_LENGTH = 3
        EXPECTED_TYPE = 4

    def __init__(self, error=-1, expected=None, actual=None, msg="Invalid Argument passed"):
        self.msg = msg
        self.error = error
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return {
            1: "Expected length to be at least {} while being {}".format(self.expected, self.actual),
            2: "Expected length to be at max {} while being {}".format(self.expected, self.actual),
            3: "Expected length to be exactly {} while being {}".format(self.expected, self.actual),
            4: "Expected type is {} while being {}".format(str(self.expected), str(self.actual)),
        }.get(self.error, self.msg)


class ConfigObject:
    def __init__(self):
        self.plain_config = {}

    def get_val(self, key, default=None):
        if key in self.plain_config:
            return self.plain_config[key]
        return default

    def to_dict(self):
        output_dict = copy.deepcopy(self.plain_config)
        for key in output_dict:
            if issubclass(type(output_dict[key]), ConfigObject):
                output_dict[key] = output_dict[key].to_dict()
        return output_dict


class RootConfigObject(ConfigObject):
    KEY_PREFIX = 'prefix'
    KEY_CONFIG = 'config'

    def __init__(self, plain_config={}):
        super().__init__()
        self.config = RouterConfig()

        for key in plain_config:
            if key == RootConfigObject.KEY_CONFIG:
                self.config = RouterConfig(plain_config[key])
            elif key == RootConfigObject.KEY_PREFIX:
                self.prefix = plain_config[key]

    @property
    def prefix(self):
        return self.get_val(Router.KEY_PREFIX)

    @prefix.setter
    def prefix(self, val):
        self.plain_config[Router.KEY_PREFIX] = val

    @property
    def config(self):
        return self.plain_config.get(RootConfigObject.KEY_CONFIG, None)

    @config.setter
    def config(self, val):
        self.plain_config[RootConfigObject.KEY_CONFIG] = val


class Router(RootConfigObject):
    KEY_NODEID = 'node-id'
    KEY_IGNORE = 'ignore'
    KEY_MEMBER_OF = 'member-of'

    def __init__(self, node_id=None, plain_config={}):
        super().__init__(plain_config)

        if node_id is not None:
            self.nodeid = sanitize_node_id(node_id)

        for key in plain_config:
            if key == Router.KEY_IGNORE:
                self.ignore = plain_config[key]
            elif key == Router.KEY_MEMBER_OF:
                self.member_of = plain_config[key]
            elif key == Router.KEY_NODEID:
                self.nodeid = plain_config[key]
            elif key in [RootConfigObject.__dict__[key] for key in RootConfigObject.__dict__ if key.startswith('KEY_')]:
                pass
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    def get_val(self, key, default=None):
        if key in self.plain_config:
            return self.plain_config[key]
        return default

    @staticmethod
    def mac_to_ip6(mac, prefix):
        prefix = str(ipaddress.ip_network(prefix).supernet(new_prefix=64)).split('/')[0].rstrip(':')
        suffix = hex(int(mac[:2], 16) ^ 0x02)[2:] + mac[2:4] + ':' + mac[4:6] + 'ff:fe' + mac[6:8] + ':' + mac[8:]
        return str(ipaddress.ip_network(prefix + ':' + suffix)).replace('/128', '')

    def get_ip6(self):
        if self.prefix is None:
            raise InvalidConfigurationError('Prefix not defined for node.')
        return Router.mac_to_ip6(self.nodeid, self.plain_config[Router.KEY_PREFIX])

    @property
    def nodeid(self):
        return self.plain_config.get(Router.KEY_NODEID, None)

    @nodeid.setter
    def nodeid(self, val):
        if not re.match('^([0-9A-Fa-f]{2}([:-])?){5}([0-9A-Fa-f]{2})$', val):
            raise InvalidArgumentError(msg="Argument has to be either the primary MAC or the NodeID")
        self.plain_config[Router.KEY_NODEID] = val

    @property
    def ignore(self):
        return self.get_val(Router.KEY_IGNORE)

    @ignore.setter
    def ignore(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[Router.KEY_IGNORE] = val

    @property
    def member_of(self):
        return self.get_val(Router.KEY_MEMBER_OF, default=[])

    @member_of.setter
    def member_of(self, val):
        if type(val) is not list:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, list, type(val))
        self.plain_config[Router.KEY_MEMBER_OF] = val

    def configure(self, router):
        config = self.config

        if self.config.hostname is not None and router.get_hostname() != self.config.hostname:
            log.info("*** Setting hostname to", config.hostname)
            router.set_hostname(config.hostname)

        # wireless config
        if config.wireless is not None:
            wireless_config = self.config.wireless

            def set_band_config(band, band_config):
                if band not in router.get_radios():
                    log.error("*** Config error: Invalid band for device: " + str(band))
                    return

                if band_config.channel != None:
                    try:
                        chan = band_config.channel
                        if router.get_radio_channel(band) != chan:
                            log.info("*** Setting", band, "GHz channel to", chan)
                            router.set_radio_channel(band, chan, wireless_config.preserve_channel)
                    except Exception as e:
                        log.error("*** Error: " + str(e))

                if band_config.mesh != None:
                    try:
                        status = band_config.mesh
                        if router.get_wireless_status(band, WIRELESS_TYPE.MESH) != status:
                            log.info("*** Setting", band, "GHz mesh to", ('ENABLED' if status else 'DISABLED'))
                            router.set_wireless_status(band, WIRELESS_TYPE.MESH, status)
                    except Exception as e:
                        log.error("*** Error: " + str(e))

                if band_config.client != None:
                    try:
                        status = band_config.client
                        if router.get_wireless_status(band, WIRELESS_TYPE.CLIENT) != status:
                            log.info("*** Setting", band, "GHz client network to",
                                     ('ENABLED' if status else 'DISABLED'))
                            router.set_wireless_status(band, WIRELESS_TYPE.CLIENT, status)
                    except Exception as e:
                        log.error("*** Error: " + str(e))

                if band_config.txpower != None:
                    try:
                        status = band_config.txpower
                        if router.get_txpower(band) != status:
                            log.info("*** Setting", band, "GHz client network to", status)
                            router.set_txpower(band, status)
                    except Exception as e:
                        log.error("*** Error: " + str(e))

            set_band_config(2, self.config.wireless.band_24)

            set_band_config(5, self.config.wireless.band_5)

            if wireless_config.private_wifi.enabled != None:
                private_wifi_config = wireless_config.private_wifi
                if private_wifi_config.enabled != None:
                    # ToDo implement private wifi (de)activation
                    pass

                if private_wifi_config.ssid != None:
                    # ToDo implement private wifi ssid
                    pass

                if private_wifi_config.password != None:
                    # ToDo implement private wifi password
                    pass

        # ssh keys
        if len(self.config.ssh_keys) > 0:
            log.info("*** Installing SSH Keys")
            router.set_sshkeys(self.config.ssh_keys)
        else:
            log.error("*** No SSH-Keys specified")

        # mesh lan
        if self.config.mesh_lan is not None and router.get_mesh_lan() != self.config.mesh_lan:
            try:
                mesh_lan = self.config.mesh_lan
                if mesh_lan != router.get_mesh_lan():
                    log.info("*** Setting mesh_lan to", ("MESH" if mesh_lan else "CLIENT"))
                    router.set_mesh_lan(mesh_lan)
            except Exception as e:
                log.error("*** Error: " + str(e))

        # mesh wan
        if self.config.mesh_wan is not None and router.get_mesh_wan() != self.config.mesh_wan:
            try:
                mesh_wan = self.config.mesh_wan
                if mesh_wan != router.get_mesh_wan():
                    log.info("*** Setting mesh_wan to", ("MESH" if mesh_wan else "DISABLED"))
                    router.set_mesh_wan(mesh_wan)
            except Exception as e:
                log.error("*** Error: " + str(e))

        # fastd
        if router.get_vpn_status() != self.config.fastd_active:
            status = self.config.fastd_active
            log.info("*** Setting fastd to", ('ENABLED' if status else 'DISABLED'))
            if self.config.fastd_active is True:
                try:
                    router.set_vpn_status(status)
                    if status == True:
                        log.info("*** Fastd config:\n\n# %s\n# %s\nkey \"%s\";\n" % (
                            router.get_hostname(),
                            ':'.join(re.findall('[0-9a-f]{2}', self.nodeid)),
                            router.get_vpn_key()))
                except Exception as e:
                    log.error("*** Error: " + str(e))
            elif self.config.fastd_active is False:
                router.set_vpn_status(False)

        if self.config.location is not None:
            log.info("*** Setting location to", ("ENABLED" if self.config.location.enabled else "DISABLED"))
            if self.config.location.enabled:
                log.info("*** Lat: {} Lon: {}".format(self.config.location.latitude, self.config.location.longitude))
            router.set_location(self.config.location.enabled, self.config.location.latitude,
                                self.config.location.longitude)

        # contact-info
        if self.config.contact is not None:
            log.info("*** Setting contact-info to", self.config.contact)
            router.set_contact(self.config.contact)

        # contact-info
        if self.config.autoupdater is not None:
            if self.config.autoupdater.enabled is not None:
                log.info("*** Setting autoupdater to", self.config.autoupdater.enabled)
            if self.config.autoupdater.branch is not None:
                log.info("*** Setting autoupdater branch to", self.config.autoupdater.branch)
            router.set_autoupdater(self.config.autoupdater.enabled, self.config.autoupdater.branch)


class Group(RootConfigObject):
    def __init__(self, group_name, plain_config={}):
        super().__init__(plain_config)
        self.group_name = group_name

        for key in self.plain_config:
            if key == Router.KEY_IGNORE:
                self.ignore = plain_config[key]
            elif key == Router.KEY_MEMBER_OF:
                self.member_of = plain_config[key]
            elif key in [RootConfigObject.__dict__[key] for key in RootConfigObject.__dict__ if key.startswith('KEY_')]:
                pass
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def ignore(self):
        return self.get_val(Router.KEY_IGNORE)

    @ignore.setter
    def ignore(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(error=InvalidArgumentError.Errors.EXPECTED_TYPE, expected=bool, actual=type(val))
        self.plain_config[Router.KEY_IGNORE] = val


class RouterConfig(ConfigObject):
    KEY_CONTACT = 'contact'
    KEY_AUTOUPDATER = 'autoupdater'
    KEY_WIRELESS = 'wireless'
    KEY_SSH = 'ssh-keys'
    KEY_LOCATION = 'location'
    KEY_HOSTNAME = 'hostname'
    KEY_FASTD_CONFIG = 'mesh-vpn'
    KEY_MESH_LAN = 'mesh-lan'
    KEY_MESH_WAN = 'mesh-wan'

    def __init__(self, plain_config={}):
        super().__init__()
        self.wireless = WirelessConfig()

        for key in plain_config:
            if key == RouterConfig.KEY_WIRELESS:
                self.wireless = WirelessConfig(plain_config[RouterConfig.KEY_WIRELESS])
            elif key == RouterConfig.KEY_SSH:
                self.ssh_keys = plain_config[RouterConfig.KEY_SSH]
            elif key == RouterConfig.KEY_LOCATION:
                self.location = LocationConfig(plain_config[RouterConfig.KEY_LOCATION])
            elif key == RouterConfig.KEY_HOSTNAME:
                self.hostname = plain_config[RouterConfig.KEY_HOSTNAME]
            elif key == RouterConfig.KEY_FASTD_CONFIG:
                self.fastd_active = plain_config[RouterConfig.KEY_FASTD_CONFIG]
            elif key == RouterConfig.KEY_MESH_LAN:
                self.mesh_lan = plain_config[RouterConfig.KEY_MESH_LAN]
            elif key == RouterConfig.KEY_MESH_WAN:
                self.mesh_wan = plain_config[RouterConfig.KEY_MESH_WAN]
            elif key == RouterConfig.KEY_CONTACT:
                self.contact = plain_config[RouterConfig.KEY_CONTACT]
            elif key == RouterConfig.KEY_AUTOUPDATER:
                self.autoupdater = AutoupdaterConfig(plain_config[RouterConfig.KEY_AUTOUPDATER])
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def hostname(self):
        return self.get_val(RouterConfig.KEY_HOSTNAME)

    @hostname.setter
    def hostname(self, val):
        self.plain_config[RouterConfig.KEY_HOSTNAME] = str(val)

    @property
    def contact(self):
        return self.get_val(RouterConfig.KEY_CONTACT)

    @contact.setter
    def contact(self, val):
        self.plain_config[RouterConfig.KEY_CONTACT] = str(val)

    @property
    def autoupdater(self):
        return self.plain_config.get(RouterConfig.KEY_AUTOUPDATER, None)

    @autoupdater.setter
    def autoupdater(self, val):
        if type(val) is not AutoupdaterConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, AutoupdaterConfig, type(val))

        self.plain_config[RouterConfig.KEY_AUTOUPDATER] = val

    @property
    def ssh_keys(self):
        return self.get_val(RouterConfig.KEY_SSH, default=[])

    @ssh_keys.setter
    def ssh_keys(self, val):
        if type(val) is not list:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, list, type(val))

        for key in val:
            if type(key) is not str:
                raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, str, type(key))

        self.plain_config[RouterConfig.KEY_SSH] = val

    @property
    def location(self):
        return self.plain_config.get(RouterConfig.KEY_LOCATION, None)

    @location.setter
    def location(self, val):
        if type(val) is not LocationConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, LocationConfig, type(val))

        self.plain_config[RouterConfig.KEY_LOCATION] = val

    @property
    def mesh_lan(self):
        return self.get_val(RouterConfig.KEY_MESH_LAN)

    @mesh_lan.setter
    def mesh_lan(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))

        self.plain_config[RouterConfig.KEY_MESH_LAN] = val

    @property
    def mesh_wan(self):
        return self.get_val(RouterConfig.KEY_MESH_WAN)

    @mesh_wan.setter
    def mesh_wan(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[RouterConfig.KEY_MESH_WAN] = val

    @property
    def fastd_active(self):
        return self.get_val(RouterConfig.KEY_FASTD_CONFIG)

    @fastd_active.setter
    def fastd_active(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[RouterConfig.KEY_FASTD_CONFIG] = val

    @property
    def wireless(self):
        return self.plain_config.get(RouterConfig.KEY_WIRELESS, None)

    @wireless.setter
    def wireless(self, val):
        if type(val) is not WirelessConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, WirelessConfig, type(val))
        self.plain_config[RouterConfig.KEY_WIRELESS] = val


class WirelessConfig(ConfigObject):
    KEY_BAND_24 = '2_4GHz'
    KEY_BAND_5 = '5GHz'
    KEY_PRIVATE_WIFI = 'private-wifi'
    KEY_PRESERVE_CHANNEL = 'preserve-channel'

    def __init__(self, plain_config={}):
        super().__init__()
        self.band_24 = BandConfig(BandConfig.BAND_24)
        self.band_5 = BandConfig(BandConfig.BAND_5)
        self.private_wifi = PrivateWiFiConfig()
        for key in plain_config:
            if key == WirelessConfig.KEY_BAND_24:
                self.band_24 = BandConfig(BandConfig.BAND_24, plain_config[WirelessConfig.KEY_BAND_24])
            elif key == WirelessConfig.KEY_BAND_5:
                self.band_5 = BandConfig(BandConfig.BAND_5, plain_config[WirelessConfig.KEY_BAND_5])
            elif key == WirelessConfig.KEY_PRIVATE_WIFI:
                self.private_wifi = PrivateWiFiConfig(plain_config[WirelessConfig.KEY_PRIVATE_WIFI])
            elif key == WirelessConfig.KEY_PRESERVE_CHANNEL:
                self.preserve_channel = plain_config[WirelessConfig.KEY_PRESERVE_CHANNEL]
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def preserve_channel(self):
        return self.get_val(WirelessConfig.KEY_PRESERVE_CHANNEL, default=False)

    @preserve_channel.setter
    def preserve_channel(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))

        self.plain_config[WirelessConfig.KEY_PRESERVE_CHANNEL] = bool(val)

    @property
    def band_24(self):
        return self.get_val(WirelessConfig.KEY_BAND_24)

    @band_24.setter
    def band_24(self, val):
        if type(val) is not BandConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, BandConfig, type(val))
        self.plain_config[WirelessConfig.KEY_BAND_24] = val

    @property
    def band_5(self):
        return self.get_val(WirelessConfig.KEY_BAND_5)

    @band_5.setter
    def band_5(self, val):
        if type(val) is not BandConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, BandConfig, type(val))
        self.plain_config[WirelessConfig.KEY_BAND_5] = val

    @property
    def private_wifi(self):
        return self.get_val(WirelessConfig.KEY_PRIVATE_WIFI)

    @private_wifi.setter
    def private_wifi(self, val):
        if type(val) is not PrivateWiFiConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, PrivateWiFiConfig, type(val))
        self.plain_config[WirelessConfig.KEY_PRIVATE_WIFI] = val

    @property
    def band_24(self):
        return self.plain_config.get(WirelessConfig.KEY_BAND_24, None)

    @band_24.setter
    def band_24(self, val):
        if type(val) is not BandConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, BandConfig, type(val))
        self.plain_config[WirelessConfig.KEY_BAND_24] = val

    @property
    def band_5(self):
        return self.plain_config.get(WirelessConfig.KEY_BAND_5, None)

    @band_5.setter
    def band_5(self, val):
        if type(val) is not BandConfig:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, BandConfig, type(val))
        self.plain_config[WirelessConfig.KEY_BAND_5] = val


class LocationConfig(ConfigObject):
    KEY_ENABLED = 'enabled'
    KEY_LATITUDE = 'latitude'
    KEY_LONGITUDE = 'longitude'

    def __init__(self, plain_config={}):
        super().__init__()
        for key in plain_config:
            if key == LocationConfig.KEY_ENABLED:
                self.enabled = plain_config[LocationConfig.KEY_ENABLED]
            elif key == LocationConfig.KEY_LATITUDE:
                self.latitude = plain_config[LocationConfig.KEY_LATITUDE]
            elif key == LocationConfig.KEY_LONGITUDE:
                self.longitude = plain_config[LocationConfig.KEY_LONGITUDE]
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def enabled(self):
        return self.get_val(LocationConfig.KEY_ENABLED, default=None)

    @enabled.setter
    def enabled(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))

        self.plain_config[LocationConfig.KEY_ENABLED] = val

    @property
    def latitude(self):
        return self.get_val(LocationConfig.KEY_LATITUDE)

    @latitude.setter
    def latitude(self, val):
        try:
            self.plain_config[LocationConfig.KEY_LATITUDE] = float(val)
        except ValueError as e:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, float, type(val))

    @property
    def longitude(self):
        return self.get_val(LocationConfig.KEY_LONGITUDE)

    @longitude.setter
    def longitude(self, val):
        try:
            self.plain_config[LocationConfig.KEY_LONGITUDE] = float(val)
        except ValueError as e:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, float, type(val))


class AutoupdaterConfig(ConfigObject):
    KEY_ENABLED = 'enabled'
    KEY_BRANCH = 'branch'

    def __init__(self, plain_config={}):
        super().__init__()
        for key in plain_config:
            if key == AutoupdaterConfig.KEY_ENABLED:
                self.enabled = plain_config[AutoupdaterConfig.KEY_ENABLED]
            elif key == AutoupdaterConfig.KEY_BRANCH:
                self.branch = plain_config[AutoupdaterConfig.KEY_BRANCH]
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def enabled(self):
        return self.get_val(AutoupdaterConfig.KEY_ENABLED, default=None)

    @enabled.setter
    def enabled(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))

        self.plain_config[LocationConfig.KEY_ENABLED] = val

    @property
    def branch(self):
        return self.get_val(AutoupdaterConfig.KEY_BRANCH, default=None)

    @branch.setter
    def branch(self, val):
        try:
            self.plain_config[AutoupdaterConfig.KEY_BRANCH] = str(val)
        except ValueError as e:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, float, type(val))


class PrivateWiFiConfig(ConfigObject):
    KEY_PRIVATE_WIFI_ENABLED = 'enabled'
    KEY_PRIVATE_WIFI_SSID = 'ssid'
    KEY_PRIVATE_WIFI_PASSWORD = 'password'

    def __init__(self, plain_config={}):
        super().__init__()
        self.plain_config = {}

        for key in plain_config:
            if key == PrivateWiFiConfig.KEY_PRIVATE_WIFI_ENABLED:
                self.enabled = plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_ENABLED]
            elif key == PrivateWiFiConfig.KEY_PRIVATE_WIFI_SSID:
                self.ssid = plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_SSID]
            elif key == PrivateWiFiConfig.KEY_PRIVATE_WIFI_PASSWORD:
                self.password = plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_PASSWORD]
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    @property
    def enabled(self):
        return self.get_val(PrivateWiFiConfig.KEY_PRIVATE_WIFI_ENABLED)

    @enabled.setter
    def enabled(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_ENABLED] = val

    @property
    def ssid(self):
        return self.get_val(PrivateWiFiConfig.KEY_PRIVATE_WIFI_SSID)

    @ssid.setter
    def ssid(self, val):
        if type(val) is not str:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, str, type(val))
        if len(val) > 32:
            raise InvalidArgumentError(InvalidArgumentError.Errors.MAX_LENGTH, 32, len(val))
        self.plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_SSID] = str(val)

    @property
    def password(self):
        return self.get_val(PrivateWiFiConfig.KEY_PRIVATE_WIFI_PASSWORD)

    @password.setter
    def password(self, val):
        if type(val) is not str:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, str, type(val))
        if len(val) < 8:
            raise InvalidArgumentError(InvalidArgumentError.Errors.MIN_LENGTH, 8, len(val))
        if len(val) > 63:
            raise InvalidArgumentError(InvalidArgumentError.Errors.MAX_LENGTH, 63, len(val))

        self.plain_config[PrivateWiFiConfig.KEY_PRIVATE_WIFI_PASSWORD] = str(val)


class BandConfig(ConfigObject):
    KEY_WIRELESS_MESH = 'mesh'
    KEY_WIRELESS_CLIENT = 'client'
    KEY_CHANNEL = 'channel'
    KEY_TXPOWER = 'txpower'
    BAND_24 = 2
    BAND_5 = 5

    def __init__(self, band, plain_config={}):
        super().__init__()
        self.plain_config = {}
        self.band = band
        if plain_config is None:
            plain_config = {}
        for key in plain_config:
            if key == BandConfig.KEY_WIRELESS_MESH:
                self.mesh = plain_config[key]
            elif key == BandConfig.KEY_WIRELESS_CLIENT:
                self.client = plain_config[key]
            elif key == BandConfig.KEY_CHANNEL:
                self.channel = plain_config[key]
            elif key == BandConfig.KEY_TXPOWER:
                self.txpower = plain_config[key]
            else:
                raise InvalidConfigurationError(key + " is not a valid config parameter")

    def to_dict(self):
        output_dict = copy.deepcopy(self.plain_config)
        return output_dict

    @property
    def channel(self):
        return self.get_val(BandConfig.KEY_CHANNEL)

    @channel.setter
    def channel(self, val):
        if (self.band == BandConfig.BAND_24 and val in range(1, 14)) or (
                        self.band == BandConfig.BAND_5 and val in range(36, 65, 4)):
            self.plain_config[BandConfig.KEY_CHANNEL] = int(val)
        else:
            raise InvalidArgumentError(msg="Invalid Channel for Band " + str(self.band) + ": " + str(val))

    @property
    def client(self):
        return self.get_val(BandConfig.KEY_WIRELESS_CLIENT)

    @client.setter
    def client(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[BandConfig.KEY_WIRELESS_CLIENT] = bool(val)

    @property
    def mesh(self):
        return self.get_val(BandConfig.KEY_WIRELESS_MESH)

    @mesh.setter
    def mesh(self, val):
        if type(val) is not bool:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, bool, type(val))
        self.plain_config[BandConfig.KEY_WIRELESS_MESH] = bool(val)

    @property
    def txpower(self):
        return self.get_val(BandConfig.KEY_TXPOWER)

    @txpower.setter
    def txpower(self, val):
        if type(val) is not int:
            raise InvalidArgumentError(InvalidArgumentError.Errors.EXPECTED_TYPE, int, type(val))
        self.plain_config[BandConfig.KEY_TXPOWER] = int(val)
