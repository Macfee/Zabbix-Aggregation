#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import time


class Api:
    def __init__(self):
        self.url = 'http://1/api_jsonrpc.php'
        self.username = "Admin"
        self.password = "zabbix"
        self.headers = {'Content-Type': 'application/json'}
        self.color = ['1A7C11', 'F63100', '2774A4', 'A54F10', 'FC6EA3', '6C59DC', 'AC8C14', '611F27', 'F230E0', '5CCD18', 'BB2A02', '5A2B57', '89ABF8', '7EC25C', '274482', '2B5429', '8048B4', 'FD5434', '790E1F', '87AC4D']
        auth = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 0,
            "auth": None,
        }
        requests.encoding = 'utf8'
        response = requests.post(self.url, data=json.dumps(auth), headers=self.headers)
        self.authid = json.loads(response.text)['result']

    def item_get(self, monitor_item, fuzzy_host_name):
        item_ids = []
        item_get = {
            "jsonrpc": "2.0",
            "method": "item.get",  # 获取主机图形的方法
            "params": {
                "output": "extend",
                "hostids": [],
                "sortfield": "name"
            },
            "id": 2,
            'auth': self.authid
        }

        item_get['params']['hostids'] = self.host_get(fuzzy_host_name)
        response = requests.post(self.url, data=json.dumps(item_get), headers=self.headers)
        graph_id = json.loads(response.text)['result']
        for i in graph_id:
            if i['name'] ==  monitor_item:
                item_ids.append(i['itemid'])
        return item_ids

    def graph_create(self, graph_name=u"xxxxx调用总数"):
        graph_create = {
            "jsonrpc": "2.0",
            "method": "graph.create",
            "params": {
                'name': graph_name,
                "width": 900,
                "height": 200,
                "gitems": [
                ]
            },

            "auth": self.authid,
            "id": 2
        }

        for value in self.graph_get():
            graph_data = dict()
            graph_data['itemid'] = value
            color = self.color
            graph_data['color'] = color[0]
            color.pop(0)
            graph_create['params']['gitems'].append(graph_data)

        response = requests.post(self.url, data=json.dumps(graph_create), headers=self.headers)
        return response.text

    def graph_update(self, monitor_item, fuzzy_host_name, graph_id, height, width):
        color = self.color
        graph_update = {

                "jsonrpc": "2.0",
                "method": "graph.update",
                "params": {
                    "graphid": graph_id,
                    "height": height,
                    "width": width,
                    "ymax_type": 1,
                    "yaxismax": 100,
                    'gitems': [
                    ]
            },

            "auth": self.authid,
            "id": 1
        }

        for value in self.item_get(monitor_item, fuzzy_host_name):
            graph_data = dict()
            graph_data['itemid'] = value
            graph_data['color'] = color[0]
            color.pop(0)
            graph_update['params']['gitems'].append(graph_data)

        response = requests.post(self.url, data=json.dumps(graph_update), headers=self.headers)
        return response.text

    def host_delete(self):
        delete_host = {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [
                "10542"
            ],
            "auth": self.authid,
            "id": 1

        },

        response = requests.post(self.url, data=json.dumps(delete_host), headers=self.headers)
        return response.text

    def get_item(self, host_id):
        item_info = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": host_id,
                "search": {
                    "key_": "system"
                },
                "sortfield": "name"
            },
            "auth": self.authid,
            "id": 1
        }

        response = requests.post(self.url, data=json.dumps(item_info), headers=self.headers)
        return response.text

    def host_get(self, server_name):
        host_id_list = []
        host_get = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "host"
                ],
                "search": {
                    "host": server_name
                }
            },
            "auth": self.authid,
            "id": 4
        }
        requests.encoding = 'utf8'
        response = requests.post(self.url, data=json.dumps(host_get), headers=self.headers)
        result = json.loads(response.text)
        if result['result'] == '':
            os.exit(1)
        for host in result['result']:
            host_id_list.append(host['hostid'])
        return host_id_list


if __name__ == "__main__":
    api = Api()
    api.graph_update(u"Outgoing network traffic on eth0", "zabbix.server.com", 5823, 200,900);
