#!/usr/bin/env python


import urllib2
from bs4 import BeautifulSoup
import os, sys

EXPECTED_AGENT = {'User-Agent': 'Mozilla/5.0'}
def find_by_title(title):
    start_url = u'http://it-ebooks.info/search/?q=%s&type=title' % title
    datas = []
    while True:
        req = urllib2.Request(start_url, None, EXPECTED_AGENT)
        soup = BeautifulSoup(urllib2.urlopen(req))
        #sorted_soup = sorted(soup.find_all('a'), key=lambda x:int(x['href'].split('/')[2]) if '/book/' in x['href'] else 0)
        for s in soup.find_all('a'):
            datas.append((s.attrs['href'],s.attrs['title']))
        next_page = soup.find('a',{'title':'Next page'})
        if next_page:
            start_url = u'%s%s' % ('http://www.it-ebooks.info',next_page['href'])
        else:
            break

    return sorted(filter(lambda x:False if '/search/' in x[0] or 'it ebooks' == x[1].lower() or 'http' in x[0] else True, set(datas)), key=lambda x:int(x[0].split('/')[-2]), reverse=False)

if __name__=='__main__':
    assert len(sys.argv)==2, 'Need search keyword.'
    found_books = find_by_title(sys.argv[1])
    assert found_books, 'No books match query.'
    for index, book in enumerate(found_books):
        print '%d - ebook-id %s - title %s' % (index+1, book[0].split('/')[-2], book[1])
    print 'found %d books' % (index+1)
    
