import ipaddress
import logging as log
import os
import re
import socket
from enum import Enum

import paramiko

from pepper import simple_logger as log


class ConfigurationEntryNotExistentError(Exception):
    pass


class WIRELESS_TYPE(Enum):
    MESH = 1
    CLIENT = 2

    def __str__(self):
        if self.value == 1: return 'mesh'
        if self.value == 2: return 'client'


class RouterConnection:
    def __init__(self, host):
        self.transport = None
        self.host = host

    def connect(self, username='root'):
        port = 22

        if ip_family(self.host) is 4:
            socket_type = socket.AF_INET
        else:
            socket_type = socket.AF_INET6

        try:
            sock = socket.socket(socket_type, socket.SOCK_STREAM)
            sock.connect((self.host, port))
        except Exception as e:
            log.error('*** Connect failed while connecting to', self.host + ':', str(e))
            raise e

        self.transport = paramiko.Transport(sock)
        try:
            self.transport.start_client()
        except paramiko.SSHException as e:
            log.error('*** SSH negotiation failed.')
            raise e

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            log.error('*** Unable to open host keys file')
            keys = {}

        # check server's host key -- this is important.
        key = self.transport.get_remote_server_key()
        if self.host not in keys:
            log.warn('*** WARNING: Unknown host key for router', self.host)
        elif key.get_name() not in keys[self.host]:
            log.warn('*** WARNING: Unknown host key for router', self.host)
        elif keys[self.host][key.get_name()] != key and self.host != '192.168.1.1':
            log.warn('*** WARNING: Host key has changed for router', self.host, '!!!')
            # sys.exit(1)

        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        if len(agent_keys) == 0:
            log.error("No ssh keys found in agent")
            raise Exception("No ssh keys found in agent")

        key_found = False
        try:
            self.transport.auth_none("root")
            key_found = True
        except paramiko.SSHException:
            pass

        if key_found is False:
            for key in agent_keys:
                try:
                    self.transport.auth_publickey(username, key)
                    key_found = True
                    break
                except paramiko.SSHException:
                    log.error('*** SSH authentication failed for host', self.host)

            if not key_found:
                log.error("*** No valid SSH key found for host ", self.host)
                raise Exception("*** No valid SSH key found for current host")

    def command(self, command, expect_failure=False):
        channel = self.transport.open_session()
        channel.exec_command(command)

        exit_status = -1
        stdout = ''
        stderr = ''
        while exit_status == -1 or channel.recv_ready() == True or channel.recv_stderr_ready() == True:
            if channel.recv_ready():
                stdout += channel.recv(4096).decode('ascii')
            if channel.recv_stderr_ready():
                stderr += channel.recv_stderr(4096).decode('ascii')
            if channel.exit_status_ready():
                exit_status = channel.recv_exit_status()

        channel.close()

        if exit_status != 0 and not expect_failure:
            log.error('*** [error] ' + command)
            log.error('*** [error] [stdout]', stdout)
            log.error('*** [error] [stderr]', stderr)

        return exit_status, stdout, stderr

    def disconnect(self):
        self.transport.close()

    def gluon_version(self):
        exit_status, stdout, stderr = self.command('cat /lib/gluon/gluon-version')
        if exit_status == 0:
            searchObj = re.search(r'v[0-9]{4}.[0-9].[0-9]', stdout)
            if searchObj == None:
                return None
            return searchObj.group()
        return None

    @staticmethod
    def gluon_version_compare(version1, version2):
        searchObj1 = re.search(r'v([0-9]{4}).([0-9]).([0-9])', version1)
        if searchObj1 == None:
            log.error('version1 is not a valid gluon version number:', version1)

        searchObj2 = re.search(r'v([0-9]{4}).([0-9]).([0-9])', version2)
        if searchObj2 == None:
            log.error('version2 is not a valid gluon version number:', version2)

        return searchObj2.group(1) > searchObj1.group(1) or \
               (searchObj2.group(1) == searchObj1.group(1) and \
                (searchObj2.group(2) > searchObj1.group(2) or \
                 (searchObj2.group(2) == searchObj1.group(2) and \
                  searchObj2.group(3) >= searchObj1.group(3))))

    def get_radios(self):
        band_to_radio = {}
        hwmodes = {
            '11g': 2,
            '11a': 5
        }
        for radio in ['radio0', 'radio1']:
            exit_status, stdout, stderr = self.command('uci get wireless.' + radio + '.hwmode',
                                                       True)
            if exit_status == 0:
                band_to_radio[hwmodes[stdout.replace('\n', '')]] = radio
        return band_to_radio

    def get_hostname(self):
        exit_status, stdout, stderr = self.command('pretty-hostname')
        if exit_status == 0:
            return stdout.replace('\n', '')
        return None

    def set_hostname(self, hostname):
        exit_status, stdout, stderr = self.command('pretty-hostname ' + hostname)
        return exit_status == 0

    def get_sshkeys(self):
        exit_status, stdout, stderr = self.command('cat /etc/dropbear/authorized_keys')
        if exit_status != 0:
            return []
        else:
            # TODO: filter empty lines
            return stdout.split('\n')[0:-1]

    def set_sshkeys(self, keys):
        exit_status, stdout, stderr = self.command(
            'echo \'' + '\n'.join(
                keys) + '\' > /etc/dropbear/authorized_keys')
        return exit_status == 0

    def get_mesh_lan(self):
        version = self.gluon_version()
        supported = self.gluon_version_compare('v2016.2.0', version)
        if not supported:
            log.error('*** Gluon version found on device is not supported:', version)
            return None

        exit_status, stdout, stderr = self.command('uci get network.mesh_lan.auto')
        if exit_status != 0:
            log.error('*** Could not detect mesh_lan status')
            return None
        return stdout.replace('\n', '') == '1'

    def set_mesh_lan(self, mesh_lan):
        version = self.gluon_version()
        supported = self.gluon_version_compare('v2016.2.0', version)
        if not supported:
            log.error('*** Gluon version found on device is not supported:', version)
            return None

        if mesh_lan == 0:
            exit_status, stdout, stderr = self.command(
                'uci set network.mesh_lan.auto=0; for ifname in $(cat /lib/gluon/core/sysconfig/lan_ifname); do uci add_list network.client.ifname=$ifname; done;')
        elif mesh_lan == 1:
            exit_status, stdout, stderr = self.command(
                'uci set network.mesh_lan.auto=1; for ifname in $(cat /lib/gluon/core/sysconfig/lan_ifname); do uci del_list network.client.ifname=$ifname; done;')
        else:
            raise Exception("Invalid value for parameter mesh_lan.")

        if exit_status != 0:
            log.error('*** Could not write mesh_lan status')
            return None

        exit_status, stdout, stderr = self.command('/etc/init.d/network reload')
        if exit_status != 0:
            log.error("*** Could not reload network config")

    def get_mesh_wan(self):
        exit_status, stdout, stderr = self.command('uci get network.mesh_wan.auto')
        if exit_status != 0:
            log.error('*** Could not detect mesh_wan status')
            return None
        return stdout.replace('\n', '') == '1'

    def set_mesh_wan(self, mesh_wan):
        if self.get_vpn_status() != False and mesh_wan == True:
            raise Exception("Don't set mesh_wan and mesh_vpn simultaneously")

        if mesh_wan == 0:
            exit_status, stdout, stderr = self.command('uci set network.mesh_wan.auto=0;')
        elif mesh_wan == 1:
            exit_status, stdout, stderr = self.command('uci set network.mesh_wan.auto=1;')
        else:
            raise Exception("Invalid value for parameter mesh_wan.")

        if exit_status != 0:
            log.error('*** Could not write mesh_wan status')
            return None

        exit_status, stdout, stderr = self.command('/etc/init.d/network reload')
        if exit_status != 0:
            log.error("*** Could not reload network config")

    def get_radio_channel(self, band):
        if band != 2 and band != 5:
            raise Exception('Band should either be "2" or "5"')

        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        exit_status, stdout, stderr = self.command('uci get wireless.' + radio + '.channel')
        return int(stdout.replace('\n', ''))

    def set_radio_channel(self, band, channel, preserve_channel=True):
        if band == 2 and channel not in range(1, 14):
            raise Exception('Invalid channel for 2,4 Ghz:', channel)
        if band == 5 and channel not in range(36, 65, 4):
            raise Exception('Invalid channel for 5 Ghz (indoor):', channel)

        # TODO caching
        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        exit_status1, _, _ = self.command(
            'uci set wireless.' + radio + '.channel=' + str(channel))
        exit_status2, _, _ = self.command(
            "uci set gluon-core.@wireless[0].preserve_channels='" + (
                '1' if preserve_channel else '0') + "'")
        exit_status3, _, _ = self.command('wifi reload')
        return exit_status1 == 0 and exit_status2 == 0 and exit_status3

    def get_txpower(self, band):
        if band != 2 and band != 5:
            raise Exception('Band should either be "2" or "5"')

        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        exit_status, stdout, stderr = self.command('uci get wireless.' + radio + '.txpower')
        return stdout.replace('\n', '')

    def set_txpower(self, band, txpower):
        # TODO caching
        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        exit_status1, _, _ = self.command(
            'uci set wireless.' + radio + '.txpower=' + str(txpower))
        exit_status2, _, _ = self.command('wifi reload')
        return exit_status1 == 0 and exit_status2

    def get_wireless_status(self, band, wireless_type):
        if not isinstance(wireless_type, WIRELESS_TYPE):
            raise Exception("wireless_type has to be an instance of WIRELESS_TYPE")

        # TODO caching
        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        _, stdout, _ = self.command(
            'uci get wireless.' + str(wireless_type) + '_' + radio + '.disabled')
        return stdout.replace('\n', '') == '0'

    def set_wireless_status(self, band, wireless_type, status):
        if not isinstance(wireless_type, WIRELESS_TYPE):
            raise Exception("wireless_type has to be an instance of WIRELESS_TYPE")

        # TODO caching
        radios = self.get_radios()
        if band not in radios:
            raise Exception("Invalid band for device: " + str(band))

        radio = radios[band]
        exit_status, _, _ = self.command(
            'uci set wireless.' + str(wireless_type) + '_' + radio + '.disabled=' + ('0' if status else '1'))
        return exit_status == 0

    def get_primary_mac(self):
        exit_status, stdout, stderr = self.command('cat /lib/gluon/core/sysconfig/primary_mac')
        if exit_status == 0:
            return stdout
        return None

    def set_configured(self, status):
        exit_status, stdout, stderr = self.command(
            'uci set gluon-setup-mode.@setup_mode[0].configured=\'' + str(
                status) + '\'')
        if exit_status == 0:
            return stdout
        return None

    def reboot(self, config_mode=False):
        exit_status, stdout, stderr = self.command('uci set gluon-setup-mode.@setup_mode[0].enabled=' + (
            '1' if config_mode else '0') + '; uci commit gluon-setup-mode; reboot')
        if exit_status == 0:
            return stdout
        return None

    def get_vpn_key(self):
        exit_status, stdout, stderr = self.command('/etc/init.d/fastd show_key mesh_vpn')
        if exit_status == 0:
            return stdout.replace('\n', '')
        return None

    def get_vpn_status(self):
        exit_status, stdout, stderr = self.command('uci get fastd.mesh_vpn.enabled')
        if exit_status == 0:
            return stdout.replace('\n', '') == '1'
        return None

    def set_vpn_status(self, status):
        vpn_status = self.get_vpn_status()

        if self.get_mesh_wan() != False and status == True:
            raise Exception("Don't set mesh_wan and mesh_vpn simultaneously")

        if vpn_status == False and status == True:
            exit_status, stdout, stderr = self.command(
                'uci set fastd.mesh_vpn.enabled=' + (
                    '1' if status else '0'))
            if exit_status != 0:
                raise Exception('Could not write mesh_vpn status')
            if self.get_vpn_key() != None:
                exit_status, stdout, stderr = self.command('/etc/init.d/fastd start')
            else:
                exit_status, stdout, stderr = self.command(
                    '/etc/init.d/fastd generate_key mesh_vpn')
            if exit_status != 0:
                raise Exception('Could not start fastd')
        elif vpn_status == True and status == False:
            exit_status, stdout, stderr = self.command(
                '/etc/init.d/fastd stop; uci set fastd.mesh_vpn.enabled=0')
            if exit_status != 0:
                raise Exception('Could not stop fastd')

    def get_location(self):
        exit_status, stdout, stderr = self.command('uci get gluon-node-info.@location[0].latitude')
        if exit_status != 0:
            raise Exception('No position set')
        latitude = stdout.replace('\n', '')
        exit_status, stdout, stderr = self.command('uci get gluon-node-info.@location[0].longitude')
        if exit_status != 0:
            raise Exception('No position set')
        longitude = stdout.replace('\n', '')
        return latitude, longitude

    def set_location(self, enabled, longitude=None, latitude=None):
        exit_status, stdout, stderr = self.command(
            'uci set gluon-node-info.@location[0].share_location=' + str((1 if enabled else 0)))

        if longitude is not None and latitude is not None:
            if not isinstance(longitude, float) or not isinstance(latitude, float):
                raise Exception("Provided coordinates are not of type float")

            exit_status, stdout, stderr = self.command(
                'uci set gluon-node-info.@location[0].latitude=' + str(longitude) +
                '; uci set gluon-node-info.@location[0].longitude=' + str(latitude))

    def get_contact(self):
        exit_status, stdout, stderr = self.command('uci get gluon-node-info.@owner[0].contact')
        if exit_status != 0:
            raise ConfigurationEntryNotExistentError()
        return stdout.replace('\n', '')

    def set_contact(self, contact_info):
        exit_status, stdout, stderr = self.command('uci set gluon-node-info.@owner[0].contact=\'{}\''
                                                   .format(contact_info))

    def get_autoupdater(self):
        exit_status, stdout, stderr = self.command('uci get autoupdater.settings.enabled')
        if exit_status != 0:
            log.error('*** Could not detect autoupdater status')
            return None, None

        autoupdater_status = stdout.replace('\n', '') == '1'

        exit_status, stdout, stderr = self.command('uci get autoupdater.settings.branch')
        if exit_status != 0:
            log.error('*** Could not detect autoupdater branch')
            return None, None

        autoupdater_branch = stdout.replace('\n', '')

        return autoupdater_status, autoupdater_branch

    def set_autoupdater(self, status=None, branch=None):
        if status is not None:
            exit_status, stdout, stderr = self.command('uci set autoupdater.settings.enabled=\'{}\''
                                                       .format(status))
        if branch is not None:
            exit_status, stdout, stderr = self.command('uci set autoupdater.settings.branch=\'{}\''
                                                       .format(branch))

    def commit(self):
        exit_status, stdout, stderr = self.command('uci commit')
        return exit_status == 0


def ip_family(addr):
    return ipaddress.ip_address(addr).version
