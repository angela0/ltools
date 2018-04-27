#!/usr/bin/env python
# coding=utf-8

import urllib2 as ul
import json
import sys


def main(word='你'):
    res = ul.urlopen("http://www.xhup.club/index.php/Xhup/Search/searchCode",
                     data="search_word={}".format(word))
    lst = json.loads(res.read())["list_dz"]
    for i in lst:
        print(i[0])
        print("---------------")
        print(u"拆　分：{}".format(i[1]))
        print(u"首　末：{}　{}".format(i[2], i[3]))
        print(u"编　码：{}　 {}".format(i[4], i[5]))
        print("===============")
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: xh <word>")
        exit(1)
    main(sys.argv[1])
