#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import sys
import shutil
import time
import datetime

def get_page(page_url):
    page = urllib2.urlopen(urllib2.Request(page_url, None, headers={'User-Agent':'Mozilla/5.0'}))
    if page:
        bkname = ''
        bklink = ''
        soup = BeautifulSoup(page)
        for alink in soup.find_all('a'):
            if 'http://filepi.com' in alink.attrs['href']:
                bkname = alink.text
                bklink = alink.attrs['href']
                break
            elif alink.attrs.has_key('id') and alink.attrs['id'] == 'dl':
                bkname = soup.h1.text.lower().replace(' ','-')
                bklink = 'http://it-ebooks.info%s' % alink.attrs['href']
                break
        else:
            raise AssertionError("Cannot find link for download.")
        print 'bklink ', bklink
        get_book(bkname+'.pdf', bklink, page_url)
    else:
        raise AssertionError("Cannot find page for download.")

def get_book(bkname_with_ext, filepi_url, page_url):
    print 'filepi_url ', filepi_url
    headers = {
        'Referer': page_url,
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        book = urllib2.urlopen(
            urllib2.Request(filepi_url, None, headers=headers)
        )
    except Exception as e:
        print filepi_url
        return
    # Call f.close() implicitly, when use with open(....)
    # print 'Found book size %s bytes, start downloading...' % (book.headers.get('content-length'))
    # now = datetime.datetime.now()
    bkname_with_ext = bkname_with_ext.lower().replace(' ','-')
    f = open(bkname_with_ext, 'wb')
    meta = book.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: {0} Bytes: {1}".format(filepi_url, file_size))
    file_size_dl = 0
    block_sz = 16*1024
    while True:
        buffer = book.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        p = float(file_size_dl) / file_size
        status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
        status = status + chr(8)*(len(status)+1)
        sys.stdout.write(status)

    f.close()
    print "Done download {}".format(bkname_with_ext)



if __name__=='__main__':
    assert len(sys.argv) == 2, "Invalid ebook-id."
    get_page('http://it-ebooks.info/book/%s/' % sys.argv[1])
