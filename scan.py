#!/usr/bin/env python3

import os
from publicsuffixlist.compat import PublicSuffixList
import re
import sys
import zipfile

psl = PublicSuffixList(open('public_suffix_list.dat'), accept_unknown=False)

for root, dirs, files in os.walk('/media/hans/240 GB/android_apk_unrated_unsorted'):
    for f in files:
        size = os.path.getsize(os.path.join(root, f))
        if size > 10000000:
            print(f, size)
        try:
            with zipfile.ZipFile(os.path.join(root, f), 'r') as apk:
                for filename in apk.namelist():
                    if filename.lower().endswith('.png'):
                        continue
                    with apk.open(filename) as intf:
                        data = intf.read()
                        m = re.search(b'[a-zA-Z0-9-][a-zA-Z0-9-.]{2,}\.[a-zA-Z]{2,}', data)
                        if m:
                            domainname = m.group(0).decode('utf-8')
                            if domainname.endswith('.android.com') \
                               or domainname.endswith('.so'):
                                pass
                            else:
                                ps = psl.publicsuffix(domainname)
                                if ps:
                                    print('domainname:', domainname, ps)
                                    pass
                        if filename.endswith('.class'):
                            if data.find(b'HostName('):
                                print('HostName', filename)
                            elif data.find(b'getByName('):
                                print('getByName', filename)
                            elif data.find(b'Socket('):
                                print('Socket', filename)
                            elif data.find(b'openConnection('):
                                print('openConnection', filename)
                        if filename.endswith('.so'):
                            m = re.search(b'gethostbyname(\(.*\))', data)
                            if m:
                                print('gethostbyname', m.group(0).decode('utf-8'))
                            m = re.search(b'MSPAsyncDns', data)
                            if m:
                                print('MSPAsyncDns', m.group(0).decode('utf-8'))              
        except zipfile.BadZipFile:
            print('skipping bad APK:')
        
