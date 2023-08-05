import requests
from bs4 import BeautifulSoup

from pepper.connection import RouterConnection


class GluonWeb:
    GLUON_IP = "192.168.1.1"

    @staticmethod
    def get_luci_mac(ip=GLUON_IP):
        info = requests.get('http://{ip}/cgi-bin/luci/admin/index/'.format(ip=ip))

        soup = BeautifulSoup(info.content, 'html.parser')
        for div in soup.find_all('div', {'class': 'cbi-value'}):
            title = div.find('div', {'class': 'cbi-value-title'})
            value = div.find('div', {'class': 'cbi-value-field'})
            if title is not None and 'mac' in title.text.lower():
                return value.text

    @staticmethod
    def store_ssh_keys(nodes, ip=GLUON_IP):
        node = nodes[GluonWeb.get_luci_mac(ip).replace(':', '')]
        keys = '\n'.join(node.config.ssh_keys)
        requests.post('http://{ip}/cgi-bin/luci/admin/remote'.format(ip=ip),
                      data={'cbid.system._keys._data': keys, 'cbi.submit': 1, 'cbi.apply': 'Absenden'})

    @staticmethod
    def configure_local(nodes):
        GluonWeb.store_ssh_keys((nodes))
        router = RouterConnection("192.168.1.1")
        router.connect()
        node = nodes[router.get_primary_mac().replace(':', '')]
        node.configure(router)
        router.set_configured(1)
        router.commit()
        router.reboot()
