import ipaddress
import json
from urllib.parse import urlparse

import requests
import yaml

from pepper.config import Router


class Community():
    def __init__(self, src_dict={}):
        self.name = src_dict.get('name', '')
        self.maps = src_dict.get('maps', [])
        self.nodelists = src_dict.get('nodelists', [])
        self.prefixes = src_dict.get('prefixes', [])
        self.nodes = src_dict.get('nodes', [])
        self.primary_prefix = src_dict.get('primary_prefix', None)
        self.short_name = src_dict.get('short_name', '')

    def to_dict(self):
        return {'name': self.name, 'maps': self.maps, 'nodelists': self.nodelists, 'prefixes': self.prefixes,
                'nodes': self.nodes, 'primary_prefix': self.primary_prefix, 'short_name': self.short_name}


class RemoteData:
    def __init__(self, use_cache=False, cache_path=None):
        self.use_cache = use_cache
        self.cache_path = cache_path

    def read_cache(self, path):
        with open(self.cache_path + path, 'r') as file:
            data = yaml.load(file.read())
            return data if data is not None else {}

    def write_data(self, path, data):
        with open(self.cache_path + path, 'w+') as file:
            file.write(yaml.dump(data, allow_unicode=True))


class FreifunkAPI(RemoteData):
    FFAPI_URL = 'https://api.freifunk.net/data/ffSummarizedDir.json'

    def __init__(self, use_cache, cache_path):
        super().__init__(use_cache, cache_path)
        self.api_data = []
        if self.use_cache:
            try:
                self.api_data = self.read_cache('api.yaml')
                return
            except FileNotFoundError as e:
                pass

    def update(self):
        result = requests.request('GET', FreifunkAPI.FFAPI_URL)
        if result.status_code is not requests.codes.OK:
            return
        self.load_api_data(result.content)
        self.clean_api_data()
        self.write_data('api.yaml', self.api_data)

    def load_api_data(self, data):
        self.api_data = json.loads(data)

    def clean_api_data(self):
        new_api_data = {}
        for community in self.api_data:
            new_api_data[community] = {}
            for key in self.api_data[community]:
                if key in ['url', 'name', 'nodeMaps']:
                    new_api_data[community][key] = self.api_data[community][key]
        self.api_data = new_api_data

    def find_communitiy(self, name):
        name = name.lower()
        if name in self.api_data:
            return {name: self.api_data[name]}

        possible_communities = {}
        for community in self.api_data:
            community_url = self.api_data[community].get('url', '').lower()
            community_name = self.api_data[community].get('name', '').lower()
            if name in community_name or name in community_url:
                possible_communities[community] = self.api_data[community]

        return possible_communities

    def get_community(self, community_name):
        if self.use_cache:
            try:
                return Community(self.read_cache(community_name + '.yaml'))
            except FileNotFoundError as e:
                pass
        community = self.build_community(community_name)
        if community is not None:
            self.save_community(community)
        return community

    def save_community(self, community):
        com = community.to_dict()
        self.write_data(community.short_name + '.yaml', com)

    def update_community(self, name):
        community = self.get_community(name)
        if community is not None:
            mapdata = None
            for url in community.nodelists:
                mapdata = query_nodelist(url)
                if mapdata is None:
                    continue
                if 'prefixes' in mapdata and len(mapdata['prefixes']) > 0:
                    community.prefixes = mapdata['prefixes']

                if 'nodes' in mapdata and len(mapdata['nodes']) > 0:
                    community.nodes = mapdata['nodes']

            if len(community.prefixes) is 0:
                for url in community.maps:
                    mapdata = query_meshviewer(url)
                    if mapdata is None:
                        continue

                    if 'prefixes' in mapdata and len(mapdata['prefixes']) > 0:
                        community.prefixes = mapdata['prefixes']

                    if 'nodes' in mapdata and len(mapdata['nodes']) > 0:
                        community.nodes = mapdata['nodes']
            if mapdata is not None:
                self.write_data(name + '.yaml', community.to_dict())
        return community

    def build_community(self, name):
        found_communities = self.find_communitiy(name)

        if len(found_communities) is not 1:
            return None

        for community_name in found_communities:
            community = Community()
            community.short_name = community_name
            community.name = found_communities[community_name]['name']
            community.maps = [x['url'] for x in found_communities[community_name].get('nodeMaps', {}) if
                              x.get('mapType', '') == 'geographical']
            community.nodelists = [x['url'] for x in found_communities[community_name].get('nodeMaps', {}) if
                                   x.get('technicalType', '') == 'nodelist']
            return community


class MapParser():
    @staticmethod
    def to_router(node):
        router = Router()
        router.nodeid = node['node_id']
        router.config.hostname = node['hostname']
        if 'position' in node:
            router.config.position.enabled = True
            router.config.position.latitude = node['latitiude']
            router.config.position.longitude = node['longitude']
        return router

    @staticmethod
    def parse(nodes):
        if isinstance(nodes, str):
            nodes = json.loads(nodes)
        if 'version' in nodes:
            if nodes['version'] == '1.0.0' or nodes['version'] == '1.0.1':
                # nodelist.json
                return MapParser.nodelist(nodes)
            elif nodes['version'] is 1:
                # Meshviewer v1
                return MapParser.meshviewer(nodes)
            elif nodes['version'] is 2:
                # Meshviewer v2
                return MapParser.meshviewer(nodes)

    @staticmethod
    def nodelist(nodes):
        if isinstance(nodes, str):
            nodes = json.loads(nodes)

        output_nodes = []
        for node in nodes['nodes']:
            n = {'node_id': node['id']}
            if 'name' in node:
                n['hostname'] = node['name']
            if 'position' in node:
                n['latitude'] = node['position']['lat']
                n['longitude'] = node['position']['long']
                output_nodes.append(n)

        return {'nodes': output_nodes}

    @staticmethod
    def meshviewer(nodes):
        if isinstance(nodes, str):
            nodes = json.loads(nodes)

        if isinstance(nodes['nodes'], dict):
            # MeshViewer 1
            nodes = [y for x, y in list(nodes['nodes'].items())]
        else:
            nodes = nodes['nodes']

        output_nodes = []
        prefixes = []
        for node in nodes:
            n = {'node_id': node['nodeinfo']['node_id']}
            if 'hostname' in node['nodeinfo']:
                n['hostname'] = node['nodeinfo']['hostname']

                if 'location' in node['nodeinfo'] and 'latitude' in node['nodeinfo']['location'] and 'longitude' in \
                        node['nodeinfo']['location']:
                    n['latitude'] = node['nodeinfo']['location']['latitude']
                    n['longitude'] = node['nodeinfo']['location']['longitude']

                if 'network' in node['nodeinfo']:
                    node_prefixes = [str(ipaddress.IPv6Network(x).supernet(new_prefix=64)) for x in
                                     node['nodeinfo']['network'].get('addresses', []) if
                                     not ipaddress.ip_address(x).is_link_local]
                    prefixes = prefixes + list(set(node_prefixes) - set(prefixes))

            output_nodes.append(n)

        return {'nodes': output_nodes, 'prefixes': prefixes}


def retrieve(url):
    response = requests.request('GET', url)
    if response.status_code is not 200:
        return []
    try:
        return json.loads(response.content)
    except Exception as e:
        return []


def query_meshviewer(url):
    url = url + ('/' if url[-1:] != '/' else '')
    response = requests.request('GET', url + 'config.json')
    if response.status_code is 200:
        config = json.loads(response.content)
        if 'dataPath' not in config:
            pass

        data_path = (config['dataPath'] if type(config['dataPath']) is str else config['dataPath'][0])

        first_part = data_path if bool(urlparse(data_path).netloc) else url + (
            data_path if data_path[0] != '/' else data_path[1:])

        data_url = first_part + ('/' if first_part[-1:] != '/' else '') + 'nodes.json'
        data = requests.request('GET', data_url)
        if data.status_code is 200:
            return MapParser.parse(data.text)
    return None


def query_nodelist(url):
    return MapParser.parse(retrieve(url))
