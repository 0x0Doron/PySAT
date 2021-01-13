#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hashlib import md5
import requests
import os


PATH = os.path.abspath(os.getcwd())
api_relative_path = '/config/api.txt'
api_full_path = PATH + api_relative_path


def read_api():
    if any_api():
        api = None
        try:
            with open(api_full_path, 'r') as f:
                lines = f.readlines()
                api = lines[0]
        except:
            pass
    return api


def any_api():
    if os.path.isfile(api_full_path):
        return True
    return False
