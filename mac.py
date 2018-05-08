#!/usr/bin/env python
# coding=utf-8

import urllib2
import sys

apiurl = "http://api.macvendors.com/{}"


def usage():
    return """usage: mac [MAC]
    MAC := 00:11:22:33:44:55 |
           00-11-22-33-44-55 |
           00.11.22.33.44.55 |
           001122334455 |
           0011.2233.4455

    """

def knowledge():
    return """MAC地址（Media Access Control Address），为媒体访问控制地址，
    也称为局域网地址（LAN Address），以太网地址（Ethernet Address）
    或物理地址（Physical Address），它是一个用来确认网络设备位置的地址。
    在OSI模型中，第三层网络层负责IP地址，第二层数据链接层则负责MAC地址。

    MAC地址共48位（6个字节），以十六进制表示。
    前24位由IEEE决定如何分配，后24位由实际生产该网络设备的厂商自行指定。
    ff:ff:ff:ff:ff:ff则作为广播地址，
    01:xx:xx:xx:xx:xx是多播地址，
    01:00:5e:xx:xx:xx是IPv4多播地址
                                     -- From Wikipedia"""


def get_ventor(macstr):
    result = "Unknow"
    try:
        resp = urllib2.urlopen(apiurl.format(macstr))
    except urllib2.HTTPError as e:
        if e.code != 404:
            result = e.msg
    else:
        result = resp.read()
    return result


def main():
    result = ""
    if len(sys.argv) >= 2:
        result = get_ventor(sys.argv[1])
    else:
        result = usage() + knowledge()

    print(result)


if __name__ == "__main__":
    main()
