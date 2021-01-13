#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyexiv2


PATH = os.path.abspath(os.getcwd())
config_relative_path = '/config/images.txt'
config_full_path = PATH + config_relative_path

# Config defaults --> folder, image limit, ...
DEFAULTS = (
    'folder:img/forensics/',
    'limit:9',
)

def get_image_config():
    ''' Gets image config as a list '''
    config = []

    with open(config_full_path) as cf:
        lines = cf.readlines()
        config.append(lines[0].split('folder:')[1])
        config.append(lines[1].split('limit:')[1])

    return config


def is_image_config():
    if os.path.isfile(config_full_path):
        return True
    return False


def remove_config():
    if is_image_config():
        os.remove(config_full_path)


def set_default_config():
    remove_config()
    set_image_config(DEFAULTS)


def get_image_folder_path():
    '''
        Returns full and abs path
    '''
    config = get_image_config()
    folder = config[0]
    full_path = PATH + folder

    return full_path, folder


def set_image_config(config):
    '''
        If txt format is:

            folder:/data/images/
            limit:9

        then the data parameter is a tuple:

            (folder, limit)
    '''
    try:
        with open(config_full_path, 'w+') as cf:
            cf.write(config[0] + os.linesep)
            cf.write(config[1] + os.linesep)

    except Exception as e:
        pass



class CustomImage:
    '''
        Our own image object to interact
        with paths and metadata in easy way
    '''

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.format = self.name.split('.')[1]
        self.exif = self._get_exif()


    def _get_exif(self):
        '''
            If image contains exif-data,
            returns dict with exif-data,
            else returns None value
        '''
        try:
            image = pyexiv2.Image(self.path)
            exif = image.read_exif()
            return self._pretty_keys(exif)
        except:
            return None


    def _pretty_keys(self, exif_dict):
        ''' Remove redundant info from exif dict keys '''
        pretty_exif = {key.split('.')[len(key.split('.'))-1]:value for (key, value) in exif_dict.items()}

        return pretty_exif
