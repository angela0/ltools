#!/usr/bin/env python
# coding=utf-8

import urllib2
import sys

apiurl = "http://cip.cc/{}"

def get_ip(ip):
    result = ""
    try:
        req = urllib2.Request(apiurl.format(ip),
                              headers={'User-Agent': 'curl/7.54.0'})
        resp = urllib2.urlopen(req)
    except Exception as e:
        result = e.message
    else:
        result = resp.read()

    return result


def main():
    ip = sys.argv[1] if len(sys.argv) >= 2 else ""
    print(get_ip(ip))

if __name__ == "__main__":
    main()
