#!/usr/bin/env python
# encoding: utf-8

import re
import appscript as AS
from glob import glob


def do_grep():
    res = set()
    for fn in glob("*.taskpaper"):
        res |= set(re.findall(r"expose\/(\d+)", open(fn).read()))
    return res


def main():
    all_ids = do_grep()

    chrome = AS.Application("Google Chrome")
    to_close = []
    for w in chrome.windows():
        for t in w.tabs():
            ids = re.findall(r"expose\/(\d+)", t.URL())
            if len(ids):
                if ids[0] in all_ids:
                    to_close.append(t)

    print "Closing %i tabs" % (len(to_close))
    for t in to_close:
        t.close()

if __name__ == '__main__':
    main()
