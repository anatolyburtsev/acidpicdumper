__author__ = 'onotole'

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'onotole'
printResult = 0
from bs4 import BeautifulSoup
import time
import urllib2
from socket import timeout
import sys
from urllib import urlretrieve
import os.path
import datetime

def loadHelper(uri):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        thing = opener.open(uri, None, 10)
        soup = BeautifulSoup(thing.read(), "lxml")
        if not (soup is None):
            return soup
        else:
            print "soup is None"
            loadHelper(uri)
    except (timeout, urllib2.HTTPError, urllib2.URLError) as error:
        sys.stdout.write("{} encountered, hold on, bro".format(error))
        sys.stdout.flush()
        time.sleep(30)
        loadHelper(uri)


def downloadPicture(link, prefix, pathDir):
    #prefix - date
    picname = link.rsplit('/',1)[1]
    picname = str(prefix) + picname
    pathToSave = os.path.join(pathDir, picname)
    print(pathToSave)
    urlretrieve(link, pathToSave)

def downloadPost(page, path2Save, postType='pic'):
    #posttype - gif for  Acid Gifdump, pic for Acid Picdump
    if postType == 'gif':
        posttypeString = 'Acid Gifdump'
    else:
        posttypeString = 'Acid Picdump'
    #TODO improve, get this information from webpage
    #prefix_date = datetime.date.today() - datetime.timedelta(days=page)
    link2Page = 'http://acidcow.com/page/'
    if page == 0: return 0
    if page == 1:
        link2Page = link2Page[:-5]
    else:
        link2Page = link2Page + str(page) + '/'
    print(link2Page)

    currentPage = loadHelper(link2Page)
    for titlefg in currentPage.find_all('div', attrs={"class":"titlefg"}):
        link = titlefg.find('a')
        #check parent for <div class="block"><h2>TOP 5 OF YESTERDAY</h2><div class="top">
        if posttypeString in link.get_text():
            picDumpLink = link.get('href')
            break

    picDumpLink = loadHelper(picDumpLink)
    for div in picDumpLink.find_all('div', attrs={"class":"silver"}):
        postDate = div.get_text().split('|')[1].strip().split()
        postDate[1] = postDate[1][:-1]
        postDate.reverse()
        prefix_date = "".join(postDate)

    for pic in picDumpLink.find_all('div', attrs={"class":"picture"}):
        picLink = pic.find('img').get('src')
        print(picLink)
        downloadPicture(picLink, prefix_date, path2Save)


def downloadPicDump(page,path2Save):
    #page 10 = http://acidcow.com/page/10/
    prefix_date = datetime.date.today() - datetime.timedelta(days=page)
    link2Page = 'http://acidcow.com/page/'
    if page == 0: return 0
    if page == 1:
        link2Page = link2Page[:-5]
    else:
        link2Page = link2Page + str(page) + '/'
    print(link2Page)

    currentPage = loadHelper(link2Page)
    for titlefg in currentPage.find_all('div', attrs={"class":"titlefg"}):
        link = titlefg.find('a')
        #check parent for <div class="block"><h2>TOP 5 OF YESTERDAY</h2><div class="top">
        if 'Acid Picdump' in link.get_text():
            picDumpLink = link.get('href')
            break

    picDumpLink = loadHelper(picDumpLink)
    for pic in picDumpLink.find_all('div', attrs={"class":"picture"}):
        picLink = pic.find('img').get('src')
        print(picLink)
        downloadPicture(picLink, prefix_date, path2Save)



if __name__ == '__main__':
    PICDIR = '/Users/onotole/yandex.disk/humordirs/ACIDPICDUMP'
    GIFDIR = '/Users/onotole/yandex.disk/humordirs/ACIDGIFDUMP'
    if not os.path.exists(PICDIR):
        os.mkdir(PICDIR)
    for i in range(2):
        print("iteration " + str(i))
        try:
            downloadPost(i, GIFDIR, 'gif')
            downloadPost(i, PICDIR, 'pic')
        except UnboundLocalError: #gifs or pics wasn't posted
            pass

