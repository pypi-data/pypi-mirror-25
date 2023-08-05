#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The class wmi_query returns a defaultdict with objects of specific class
# 

import wmi_conn
from collections import defaultdict


class wmi_query(object):

    def __init__(self, opts):
        self.user = opts['user']
        self.password = opts['password']
        self.host = opts['address']
        self.domain = opts['domain']
        self.namespace = opts['namespace']
        self.query = opts['query']
        self.delimiter = "|"
        self.data_dict = defaultdict(lambda: False)
        self.dict_name = ""

    def get_wmi_data(self):
        """
        Get a list of wmi objects from wmi_conn and process the list into a default dict.
        """
        _wmi_data = wmi_conn.wmi_conn(self.host, self.user, self.password, self.domain, self.namespace, self.query)
        _cont = 0
        self.dict_name = _wmi_data[0].getClassName()
        self.data_dict[self.dict_name] = defaultdict()
        for data in _wmi_data:
            self.data_dict[self.dict_name][_cont] = defaultdict(lambda: False)
            data_properties = data.getProperties()
            for item in data_properties:
                self.data_dict[self.dict_name][_cont][item] = data_properties[item]['value']
            _cont = _cont + 1

    def get_item(self, item_name, value_name):
        """
        Return an entire object based in the value of the specific key passed with arguments.
        Ex: object.get_item('OS_Name', 'Windows 10')
        Will return each object with OS_Name like Windows 10.
        """
        return [self.data_dict[self.dict_name][x] for x, y in enumerate(self.data_dict[self.dict_name])
                if value_name in self.data_dict[self.dict_name][x][item_name]]

    def get_items(self, item_name):
        """
        Return only item passed with arguments for each object founded by the query.
        Eg: object.get_items('OS_Name')
        """
        return set([self.data_dict[self.dict_name][x][item_name] for x, y in enumerate(self.data_dict[self.dict_name])])

    def get_item_keys(self):
        """
        Return all keys of the object founded by the query.
        """
        return [x for x in self.data_dict[self.dict_name][0]]

    def name(self):
        """
        Return the class name research by the query.
        """
        return self.dict_name

    def run(self):
        self.get_wmi_data()
