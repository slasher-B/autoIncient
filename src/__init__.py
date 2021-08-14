import re
import os
import sys
import time
import json
import socket
import logging
import requests
import subprocess
import configparser
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
banner = '  ______               __                ______                      __                       __\n' +\
         ' /      \             |  \              |      \                    |  \                     |  \ \n' +\
         '|  $$$$$$\ __    __  _| $$_     ______   \$$$$$$ _______    _______  \$$  ______   _______  _| $$_\n' +\
         '| $$__| $$|  \  |  \|   $$ \   /      \   | $$  |       \  /       \|  \ /      \ |       \|   $$ \ \n' +\
         '| $$    $$| $$  | $$ \$$$$$$  |  $$$$$$\  | $$  | $$$$$$$\|  $$$$$$$| $$|  $$$$$$\| $$$$$$$\\$$$$$$ \n' +\
         '| $$$$$$$$| $$  | $$  | $$ __ | $$  | $$  | $$  | $$  | $$| $$      | $$| $$    $$| $$  | $$ | $$ __\n' +\
         '| $$  | $$| $$__/ $$  | $$|  \| $$__/ $$ _| $$_ | $$  | $$| $$_____ | $$| $$$$$$$$| $$  | $$ | $$|  \ \n' +\
         '| $$  | $$ \$$    $$   \$$  $$ \$$    $$|   $$ \| $$  | $$ \$$     \| $$ \$$     \| $$  | $$  \$$  $$\n' +\
         ' \$$   \$$  \$$$$$$     \$$$$   \$$$$$$  \$$$$$$ \$$   \$$  \$$$$$$$ \$$  \$$$$$$$ \$$   \$$   \$$$$ \n' +\
         '                                                                                             (v1.0)\n' +\
         '                                                                                       Author:__B__\n' +\
         '-----------------------------------------------------------------------------------------------------\n'
