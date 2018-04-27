#! /usr/bin/env python
# -*- coidng: utf-8 -*-

# base on chenyao's ydcl, add sqlite cache

from __future__ import print_function

import os
import sys
import sqlite3
import getpass

if sys.version_info[0] == 2:
    PY2 = True
else:
    PY2 = False

if PY2:
    import httplib as hc
    from urllib import urlencode
else:
    import http.client as hc
    from urllib.parse import urlencode

import argparse
import json

def query(words):
    cursor = conndb.execute("select chinese from words where word='{0}'".format(words))
    first = cursor.fetchone();
    if first:
        print(first[0])
        return

    params = {
        "keyfrom": "twordterminal",
        "key": "1557945862",
        "type": "data",
        "doctype": "json",
        "version": "1.1",
        "q": words,
    }

    url = "/openapi.do?" + urlencode(params)
    conn = hc.HTTPConnection("fanyi.youdao.com")
    conn.request("GET", url)
    rep = conn.getresponse()
    data = rep.read()
    conn.close()

    data = data.decode("utf-8")
    data = json.loads(data)
    parse(data)


def parse(res):
    if res["errorCode"]:
        print("erroCode = %d\n" % res["errorCode"])
        return

    text = ur''''''
    if "basic" in res:
        text += "Basic:\n"
        basic = res["basic"]
        if "uk-phonetic" in basic: text += u"    uk-phonetic: %s\n" % basic["uk-phonetic"]
        if "us-phonetic" in basic: text += u"    us-phonetic: %s\n" % basic["us-phonetic"]
        if "phonetic" in basic: text += u"    phonetic: %s\n" % basic["phonetic"]
        if "explains" in basic:
            cnt = 1;
            for explain in basic["explains"]:
                text += u"    %s." % cnt + explain + '\n'
                cnt += 1

    if "translation" in res:
        text += "Translation:\n"
        for line in res["translation"]:
            text += u"    " + line + "\n"

    if "web" in res:
        text += "Web:\n"
        for item in res["web"]:
            text += u"    %s:\n" % item["key"]
            text += u"        "
            for trans in item["value"]:
                text += "%s; " % trans
            text += "\n"

    print(text)

    try:
        conndb.execute(u"insert into words(word, chinese) values(?, ?)", (words, text))
        conndb.commit()
    except:
        pass


def init_db():
    prefix = '/Users/' if sys.platform == 'darwin' else '/home/'
    datapath = os.path.join(prefix, '{0}/.local/data/ydcl/'.format(getpass.getuser()))

    if not os.path.exists(datapath):
        os.popen('mkdir -p '+datapath)

    global conndb
    conndb = sqlite3.connect(datapath+'ydcl.db', 1)
    conndb.execute("""
            create table if not exists words(
            id integer primary key not null,
            word varchar(50) not null,
            chinese text not null
            );
    """)


def main(word):
    query(word)

if __name__ == "__main__":
    init_db()
    parser = argparse.ArgumentParser()
    parser.add_argument("words")
    args = parser.parse_args()
    words = args.words

    main(words)
