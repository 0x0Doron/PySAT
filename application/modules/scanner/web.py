#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import requests.exceptions
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import sys
from flask_socketio import SocketIO, send, emit
import os
from collections import deque
import re



PATH = PATH = os.path.abspath(os.getcwd())
static_img_path = PATH.split('/modules/scanner')[0] + '/static/img/forensics'


def image_downloader(site, proxy=None):

    response = requests.get(site)

    parse = BeautifulSoup(response.text, 'html.parser')

    image_tags = parse.find_all('img')

    images = [url.get('src') for url in image_tags]

    if not images:
        sys.exit('Found no images')

    images = [urlparse.urljoin(response.url, url) for url in images]
    print('Found {} images'.format(len(images)))

    for url in images:
        r = requests.get(url, stream=True)
        f = open(static_img_path+'/{}'.format(url.split('/')[-1]), 'wb')
        f.write(r.content)
        f.close()
        print('Downloaded {}'.format(url))
        emit('img scan web', url)



def email_gathering(site, proxy=None):

    urls = deque([site])

    scraped_urls = set()

    # crawled_emails
    emails = set()

    # Scrap urls one by one until queue is empty
    while len(urls):
        # move next url from the queue to the set of scraped urls
        url = urls.popleft()
        scraped_urls.add(url)

        # Get base url (from relative links to absolute links)
        parts = urlparse.urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # get url's content
        print('Scraping {}'.format(url))
        try:
            if proxy is not None:
                ip = proxy[0]
                port = porxy[1]
                proxies = {'http':'http://'+ip+':'+port}

                response = requests.get(url, proxies=proxies)
            else:
                response = requests.get(url)

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore errors
            pass

        # search for emails inside the response
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        if new_emails:
            for email in new_emails:
                emit('email scan web', email)

        #### find and procces all the anchors
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all("a"):
            # extract link url
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue
            if not link in urls and not link in scraped_urls:
                urls.append(link)




def check_4_insecure_cookies(site, proxy=None):

    try:
        if proxy is not None:
            ip = proxy[0]
            port = porxy[1]
            proxies = {'http':'http://'+ip+':'+port}

            req = request.get(site, proxies=proxies)

    except:
        pass

    req = requests.get(site)

    data = ''

    for cookie in req.cookies:
        print('Name:', cookie.name)
        print('Value:', cookie.value)
        data += 'Name: ' + str(cookie.name) + '\nValue: ' + str(cookie.value)
        if not cookie.secure:
            cookie.secure = '\x1b[31mFalse\x1b[39;49m'
            print('Secure:', cookie.secure)
            data += '\nSecure: ' + str(cookie.secure)
        if 'httponly' in cookie._rest.keys():
            cookie.httponly = 'True'
        else:
            cookie.httponly = 'False'
            print('HTTPOnly:', cookie.httponly)
            data += '\nHTTPOnly: ' + str(cookie.httponly)
        if cookie.domain_initial_dot:
            cookie.domain_initial_dot = 'True'
            print('Loosly defined domain:', cookie.domain_initial_dot, '\n')
            data += '\nFreely defined domain: ' + str(cookie.domain_initial_dot)

        emit('insec cookie scan web', data)

#
#
# def trace_xss():
#
#     verbs = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE',
#     'TEST']
#     for verb in verbs:
#         req = requests.request(verb, 'http://vidiistudio.site')
#         print(verb, req.status_code, req.reason)
#         if verb == 'TRACE' and 'TRACE / HTTP/1.1' in req.text:
#             print ('Possible Cross Site Tracing vulnerability found')
#
# def testing_insecure_headers():
#     pass
