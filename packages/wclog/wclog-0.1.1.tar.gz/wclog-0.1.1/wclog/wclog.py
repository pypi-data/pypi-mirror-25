#!/usr/bin/env python
# encoding: utf-8

import requests
import config
import os, commands
import base64

def postfile(filename):
    print config.PATH + filename
    rc, user = commands.getstatusoutput('whoami')
    rc, hostname = commands.getstatusoutput('hostname')
    d = {'user': user, 'host': hostname}
    files = {'file': open(config.PATH + filename, 'rb')}
    url = 'http://' + config.IP + ':' + str(config.PORT)
    r = requests.post(url, data=d, files=files)
    print r.url,r.text

def poststring(string):
    rc, user = commands.getstatusoutput('whoami')
    rc, hostname = commands.getstatusoutput('hostname')
    url = 'http://' + config.IP + ':' + str(config.PORT)
    d = {'user': user, 'host': hostname, 'content': string}
    r = requests.post(url, data=d)
    print r.url,r.text

def logging(string):
    poststring(base64.encodestring(string))

def show(filename):
    postfile(filename)

'''
def parser():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-s", "--string", dest="string", help="Put a string to server.")
    parser.add_option("-f", "--filename", dest="file", help="Put a file to server")
    (options, args) = parser.parse_args()
    if options.string:
        poststring(options.string)
    elif options.file:
        postfile(options.file)
'''
