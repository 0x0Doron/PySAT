#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#   This module tries to get a list of available poxies
#   to hide the real IP of the client.
#
#   We will be using the third party library 'proxyscrape' ==> pip install proxyscrape
#

import proxyscrape

collector = proxyscrape.create_collector('proxy-collector', 'http')
#countries = ('spain', 'united states', 'france', 'italy', 'russia', 'china')


# This class provides the utilities to take a proxy ip:port
# and configure the browser to connect to it and give us
# an extra privicy while doing our tasks...

class CustomProxy:

    def __init__(self, ip, port, country, anonymous):
        self.ip = ip
        self.port = port
        self.country = country
        self.anonymous = anonymous


    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def country(self):
        return self._country

    @property
    def anonymous(self):
        return self._anonymous


    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @port.setter
    def port(self, port):
        self._port = port

    @country.setter
    def country(self, country):
        self._country = country

    @anonymous.setter
    def anonymous(self, anonymous):
        self._anonymous = anonymous

    def __str__(self):
        return f'CustomProxy ip: {self.ip}, port: {self.port}, country: {self.country}, anonymous: {self.anonymous}'

    def __repr__(self):
        return f'CustomProxy(ip={self.ip}, port={self.port}, country={self.country}, anonymous={self.anonymous})'


#################################################

def get_proxy(country, anon=False):
    proxy_list = collector.get_proxy({'country':country, 'anonymous':anon})
    return proxy_list


def get_proxy_list(country=None):
    '''
        Asks for a list of dictionary proxies
        and return another list but with CustomProxy objects.
    '''
    if country:
        proxies = collector.get_proxies({'country':country})
    else:
        proxies = collector.get_proxies()

    proxies = [CustomProxy(proxy_dict.host, proxy_dict.port, proxy_dict.country, proxy_dict.anonymous) for proxy_dict in proxies]
    #collector.refresh_proxies(force=True)
    return proxies
