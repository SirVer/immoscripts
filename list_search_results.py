#!/usr/bin/env python
# encoding: utf-8

from glob import glob
import appscript as AS
from urllib2 import urlopen
import re
import time
import urlparse

import close_known

import subprocess

def get_clipboard():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = p.stdout.read()
    return data

def get_source(chrome, tab):
    tab.view_source()
    time.sleep(.5)
    t = chrome.windows[1].active_tab()

    while t.loading():
        time.sleep(.1)
    t.select_all()
    t.copy_selection()
    time.sleep(1)
    rv = get_clipboard()
    t.close()
    return rv

def find_search_urls(url, source):
    paths = [ token for token in url.split("/") if
            re.match("P-\d+", token) is None ]
    idx = paths.index("S-T")
    urls = []
    for i in range(1, 99 + 1):
        new_paths = paths[:]
        new_paths.insert(idx + 1, "P-%i" % i)
        urls.append("/".join(new_paths))
    return urls

def do_grep(page_source):
    return set(re.findall(r"\/expose\/(\d+)", page_source))


def main():
    chrome = AS.Application("Google Chrome")
    to_close = []
    search_ids = set()
    for w in chrome.windows():
        for t in w.tabs():
            url = t.URL()
            if "Suche" in url and "immobilienscout" in url:
                urls = find_search_urls(url, get_source(chrome, t))
                for url in urls:
                    code = urlopen(url).read()
                    old_len = len(search_ids)
                    search_ids.update(do_grep(code))
                    if old_len == len(search_ids):
                        break

    all_known_ids = close_known.do_grep()
    remaining = search_ids - all_known_ids
    for expose_id in sorted(remaining):
        print "http://www.immobilienscout24.de/expose/%s" % expose_id

    print "Found %i search results. %i are unknown." % (len(search_ids), len(remaining))

if __name__ == '__main__':
    main()
