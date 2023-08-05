# -*- coding: utf-8 -*-

import os
import re
import json
import sys
import time
import platform
import requests
import urlparse

from bs4 import BeautifulSoup

def create_ilovejkf_and_username_folder(username):
    """
    create folder and username folder
    """

    system = platform.system()
    if system == 'Darwin':
        picfolder = 'Pictures'
    elif system == 'Windows':
        release = platform.release()
        if release in ['Vista', '7', '8']:
            picfolder = 'Pictures'
        elif release is 'XP':
            picfolder = os.path.join('My Documents', 'My Pictures')
        else:
            picfolder = ''
    else:
        picfolder = ''

    home = os.path.expanduser("~")
    base_folder = os.path.join(home, picfolder, 'ilovejkf')

    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    folder = os.path.join(base_folder, "%s" % (username))

    if not os.path.exists(folder):
        os.mkdir(folder)

    return folder

def ilovejkf(url):
    print 'start fetch url: %s' %(url)

    r = requests.get(
        url=url,
        headers={
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        }
    )

    soup = BeautifulSoup(r.content, 'html.parser')

    tid         = re.match('thread-(\d+)-1-1\.html', url.rsplit('/')[-1]).group(1)
    title       = soup.find_all('h1')[0].string
    elements    = soup.find_all('ignore_js_op')
    folder      = create_ilovejkf_and_username_folder(tid + ' ' + title)

    for element in elements:
        image = element.find('img')
        filename = image['zoomfile'].rsplit('/', 1)[1].split('?')[0]

        if ('http' or 'https') in image['zoomfile']:
            resp = requests.get(image['zoomfile'])
        else:
            resp = requests.get('https://www.jkforum.net' + image['zoomfile'])
        print 'fetch %s' % (filename)

        with open(os.path.join(folder, filename), 'wb+') as f:
            f.write(resp.content)

    print 'Winter is comming'

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit('Please provide URL from jkforum')

    ilovejkf(url)
