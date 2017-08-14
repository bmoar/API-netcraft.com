#!/usr/bin/env python
"""
This is the (unofficial) Python API for netcraft.com Website.
Using this code, you can retrieve subdomains

"""
import requests
import re
from bs4 import BeautifulSoup
import hashlib
import urllib
import math


class NetcraftAPI():
    """
        NetcraftAPI Main Handler
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

    def display_message(self, s):
        if (self.verbose):
            print('[verbose] %s' % s)

    def search(self, domain):
        res = []

        url = "http://searchdns.netcraft.com/?restriction=site+contains&host=*.%s&lookup=wait..&position=limited" % domain
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        s = requests.session()
        req = s.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")

        pattern = 'Found (\d+) site'
        number_results = re.findall(pattern, req.content.decode('utf-8'))

        if (len(number_results) > 0 and number_results[0] != '0'):
            number_results = int(number_results[0])
            self.display_message("Found %s results" % number_results)
            number_pages = int(math.ceil(number_results / 20)) + 1

            pattern = 'rel="nofollow">([a-z\.\-A-Z0-9]+)<FONT COLOR="#ff0000">'
            subdomains = re.findall(pattern, req.content.decode('utf-8'))
            res.extend(subdomains)
            last_result = subdomains[-1]

            for index_page in range(1, number_pages):
                url = "http://searchdns.netcraft.com/?host=*.%s&last=%s.%s&from=%s&restriction=site contains&position=limited" % (domain, last_result, domain, (index_page * 20 + 1))
                req = s.get(url, headers=headers)
                pattern = 'rel="nofollow">([a-z\-\.A-Z0-9]+)<FONT COLOR="#ff0000">'
                subdomains = re.findall(pattern, req.content.decode('utf-8'))
                res.extend(subdomains)
                for subdomain in subdomains:
                    self.display_message('[!] Found: %s ' % subdomain)
                last_result = subdomains[-1]
            return res
        else:
            self.display_message("No results found for %s" % domain)
            return res

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.exit("NetcraftAPI.py DOMAIN")
    else:
        for i in NetcraftAPI().search(sys.argv[1]):
            print(i)
