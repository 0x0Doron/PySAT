#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#   Bunch of methods to interact with different PySAT modules
#   and avoid the overload in app.py file
#

import sys
import os
import urllib.request
from urllib.request import build_opener, HTTPCookieProcessor

from modules.anon.anon_proxy import CustomProxy
from modules.scanner import web

import requests
import re
import getpass
from flask_socketio import SocketIO, send, emit
import threading



PATH = os.path.abspath(os.getcwd())
relative_path = '/modules/anon/config/proxy.txt'
proxy_conf_path = PATH + relative_path
wan_ip_services = ('https://ident.me',) # add more to increase the availability


######## SYSTEM ###############

def get_pc_user():
    return getpass.getuser()


def is_linux():
    if 'linux' in sys.platform.lower():
        return True
    return False


def able_4_networking():
    ''' 4 the moment only works 4 Linux'''
    if is_linux() and os.getuid() == 0:
        return True
    return False



####### ANONYMOUS MODE #########


def config_proxy(proxy):
    '''
        Creates the new config
        file with the proxy
        specifications
    '''
    try:
        with open(proxy_conf_path, 'w+') as cf: # config file
            cf.write('ip:'+proxy.ip + os.linesep)
            cf.write('port:'+proxy.port+ os.linesep)
            cf.write('country:'+proxy.country+ os.linesep)
            cf.write('anonymous:'+proxy.anonymous+ os.linesep)
    except:
        pass


def get_real_ip():
    wan_ip = urllib.request.urlopen(wan_ip_services[0]).read().decode('utf-8')
    return wan_ip


def any_proxy():
    ''' checks for proxy.txt conf file '''
    if os.path.isfile(proxy_conf_path):
        return True
    return False


def remove_proxy():
    if any_proxy():
        try:
            os.remove(proxy_conf_path)
        except:
            pass

def get_current_proxy():

    '''
        Reads and parses the data from proxy.txt
        and return an CustomProxy class object.
    '''

    data = []

    with open(proxy_conf_path) as cf:
        lines = cf.readlines()
        data.append(lines[0].split('ip:')[1])
        data.append(lines[1].split('port:')[1])
        data.append(lines[2].split('country:')[1])
        data.append(lines[3].split('anonymous:')[1])
    current_proxy = CustomProxy(data[0], data[1], data[2], data[3])
    return current_proxy


def test_proxy_connection(proxy):

    try:
        proxy_host = '{}:{}'.format(proxy.ip, proxy.port)
        req = urllib.request.Request(wan_ip_services[0], headers={'User-Agent': 'Mozilla'})
        req.set_proxy(proxy_host, 'http')
        proxy_ip = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')

        return True

    except:
        return False


def is_ip_port(addr):
    ''' Regular expression for <ip:port> '''
    match = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', addr)
    return match

################ forensics ################

def get_images(limit=None):
    '''
        Returns a tuple
        with only the name and full path+name
    '''
    images = []

    if limit is not None:
        pass
    else:

        images_path = PATH + '/application/static/img/forensics/'

        images = [filename for filename in os.listdir(images_path)]
        images_full_path = [images_path+img_name for img_name in images]    # for exif analysis
    return images, images_full_path


########## SERVER SCANNER ################

def parse_server_scanner_data(host):
    try:
        data = host.split(':')
        size = len(data)

        ipgps = None        # flag
        ip = None
        start_port = None
        finish_port = None
        conectivity = None

        if size == 4:
            ip = data[0]
            start_port = int(data[1])
            finish_port = int(data[2])
            conectivity = float(data[3])
        elif size == 5:
            ip = data[0]
            start_port = int(data[1])
            finish_port = int(data[2])
            ipgps = data[3]
            conectivity = float(data[4])
        else:
            return None

        result = (ipgps, ip, start_port, finish_port, conectivity)

        return result

    except:
        return None

############ WEB SCANNER #######################



def load_web_scanner(params):
    '''
        Checks the params list and loads the corresponding
        scan as an independent thread
        FIRST PARAMETER ALWAYS THE http/s : SITE URL
    '''
    proxy = None

    if any_proxy():
        proxy = get_current_proxy()

    site = params[0] + ':' + params[1]

    if 'image_downloader' in params:
        web.image_downloader(site, proxy)
    if 'email_gathering' in params:
        web.email_gathering(site, proxy)
    if 'insecure_cookies' in params:
        web.check_4_insecure_cookies(site, proxy)

    emit('finish', 'end')



###############################################
