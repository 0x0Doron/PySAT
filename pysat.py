#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Inits the app with pywebview web engine

import os
import time
import sys
from threading import Thread

import webview


PATH = os.path.abspath(os.getcwd())
pysat_path = PATH + '/application/app.py'

# ANSI escape sequences 4 colored prints
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def init_web_server(path):
    ''' Initializes the flask wsgi app '''
    os.system(f"python {path}")


def init_pywebengine():
    print("\n\n Loading the webengine...\n\n")
    time.sleep(4)
    try:
        webview.create_window('PySAT | IT Service Analysis Tool', 'http://localhost:5000/')
        webview.start()
    except:
        # It may throw and exception related with a 'gi' named component that is missing. But it runs anyway.
        print(f"{bcolors.WARNING}Error with pywebview engine.{bcolors.ENDC}")
        print(f"Enter {bcolors.OKGREEN}(http://localhost:5000){bcolors.ENDC} into your web browser")



def main():

    with open(PATH+'/application/header.txt', 'r') as f:
        header = f.read()
        print(f"\n{header}")
        print(f"\n\n    Coded with {bcolors.FAIL}LOVE{bcolors.ENDC} by Aritz.")
        print("----------------------------------\n\n")

    try:
        t = Thread(target=init_web_server, args=(pysat_path,))
        t.start()
        init_pywebengine()

    except:
        print("Unable to start the application. Check yout requiremnts and system dependencies.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
        sys.exit()
