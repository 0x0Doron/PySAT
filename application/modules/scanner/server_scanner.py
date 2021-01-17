#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# The CustomPortScanner class is being based on the 'How to create an efficient por scanner'
# section from the book 'Python penetration testing essentials'.
#

from modules.scanner.IPGeolocation import IPGeolocationAPI
from modules.scanner.IPGeolocation import GeolocationParams

import socket
import sys
import re
import threading
import time
from datetime import datetime


DEFAULT = (44.397, -50.644)     # default lat/long
IPGEO_API_KEY = '5bca6068e0f543e6bb8c955789cb585e'
ipgeolocationAPI = IPGeolocationAPI(IPGEO_API_KEY)
geolocation = ipgeolocationAPI.getGeolocation()

########## UTILITIES ###########################################################

def is_ip(host):
    result = re.findall(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', host)
    if result:
        return True
    return False


def dns_to_ip(host):
    if not is_ip(host):
        return socket.gethostbyname(host)
    return host


def simple_bg(ip, port):
    ''' Simple implementatio o f a port banner grabber '''
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        sock.settimeout(5)
        banner = sock.recv(1024).decode('utf-8')

        return banner
    except:
        try:
            sock = socket.socket()
            sock.connect((ip, port))
            sock.settimeout(5)
            headers = "GET / HTTP/1.1\r\n" +f"Host: {ip}\r\n" +"User-Agent: python-custom-script/2.22.0\r\n" +"Accept-Encoding: gzip, deflate\r\nAccept: */*\r\n" +"Connection: keep-alive\r\n\r\n"
            sock.send(headers.encode())
            banner = sock.recv(250).decode('utf-8')

            return banner
        except:
            return 'Unknwon service'


def get_gps(host):
    ''' Return Latitude and Longitude from IP address '''
    try:
        ip = dns_to_ip(host)

        geolocationParams = GeolocationParams()
        geolocationParams.setIPAddress(ip)
        geolocationParams.setLang('es')
        geolocation = ipgeolocationAPI.getGeolocation(geolocationParams)
        return geolocation['latitude'], geolocation['longitude']

    except:
        return DEFAULT


################################################################################

open_ports = [] # global, so we need to clear in every request
bg_data = [] # another global 'banner grabber data'

class CustomPSThread(threading.Thread):
    ''' Custom Port Scanner Thread '''

    def __init__(self, name, host, start_port, finish_port, conectivity):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.start_port = start_port
        self.finish_port = finish_port
        self.conectivity = conectivity

    def get_results(self):
        return results

    def run(self):
        scantcp(self.name, self.host, self.start_port, self.finish_port, self.conectivity)


def scantcp(name, host, start_port, finish_port, conectivity):

    try:
        for port in range(start_port, finish_port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(conectivity)
            result = sock.connect_ex((host, port))

            if result == 0:
                banner = simple_bg(host, port)
                #print(f"Port open:--------->\t{port} --- {banner}")
                open_ports.append(str(port))
                bg_data.append(banner)
            sock.close()

    except KeyboardInterrupt:
        print('Stoped')
        sys.exit()

    except socket.gaierror:
        print('Host name could not be resolve')
        sys.exit()

    except socket.error:
        print('could not connect to server')
        sys.exit()



def load_port_scanner(host, start_port, finish_port, conectivity):
    global open_ports
    global bg_data

    open_ports = []
    bg_data = []

    # print('*'*60)
    # print(' \tWlcome this is the CustomPortScanner\n')

    host = dns_to_ip(host)
    #
    # print(f'\t Scanner working on  {host}')
    # print('*'*60)

    t1 = datetime.now()
    total_ports = finish_port - start_port    # total ports

    total_ports_by_thread = 30 # number of ports handled by one thread
    total_threads = total_ports//total_ports_by_thread    # number of threads

    if(total_ports%total_ports_by_thread != 0):
        total_threads += 1

    if (total_threads > 300):
        total_ports_by_thread = total_ports//300
        total_threads += 1
        total_ports_by_thread = total_ports//total_threads

        if(total_ports%total_ports_by_thread != 0):
            total_threads += 1


    threads = []


    try:
        for i in range(total_threads):
            k = i
            finish_port = start_port+total_ports_by_thread
            name = f'T{i}'
            thread = CustomPSThread(name, host, start_port, finish_port, conectivity)
            thread.start()
            threads.append(thread)
            start_port = finish_port

    except Exception as e:
        print(f'Error: unable to start thread --> {e}')
    #
    # print(f'\t Number of Threads active: {threading.activeCount()}')

    for t in threads:
        t.join()
    print('Exiting Main Thread')
    t2 = datetime.now()

    total = (t2-t1).total_seconds()

    scan_info = {
            'threads':total_threads,
            'ports':open_ports,
            'time':total,
            'banner':bg_data
        }

    # print(f'Scanning complete in {total}')

    return scan_info

################################################################################
