#!/usr/bin/env python
# coding=utf-8

import urllib2
import sys
import json



def usage():
    return '''usage: tcron <times> "<cron time>"

    example: tcron 8 "0 */12 * * *"
             tcron 8 "@yearly"'''


def knowladge():
    return '''About crontab:
    0    2    *    *    6
    *    *    *    *    *    *
    -    -    -    -    -    -
    |    |    |    |    |    |
    |    |    |    |    |    + year [optional]
    |    |    |    |    +----- day of week (0 - 7) (Sunday=0 or 7)
    |    |    |    +---------- month (1 - 12)
    |    |    +--------------- day of month (1 - 31)
    |    +-------------------- hour (0 - 23)
    +------------------------- min (0 - 59)
    '''


def cron(args):
    data = "c={}&t={}".format(''.join(args[1:]), args[0])
    try:
        ret = urllib2.urlopen("http://www.atool.org/include/crontab.inc.php",
                              data).read()
        ret = json.loads(ret)
        message = ret['c'] if ret['r'] == 0 else '\n'.join(ret['c'])
    except Exception as e:
        message = e.message
    finally:
        return message


def main():
    if len(sys.argv) == 1:
        print("{} \n\n{}".format(usage(), knowladge()))
    elif len(sys.argv) == 3:
        print(cron(sys.argv[1:]))
    else:
        print(usage())


if __name__ == "__main__":
    main()
