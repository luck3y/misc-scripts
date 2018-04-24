#
# example usage: python mvn-force-mirror.py org/jboss/galleon/galleon-core/1.0.0.Alpha5/
#

from bs4 import BeautifulSoup
from urlparse import urlparse

import requests
import urllib2
import sys

path = sys.argv[1]
url = 'nexus/content/groups/public/'
master = 'origin-repository.jboss.org'

p1 = 'proxy01-repository.jboss.org'
p2 = 'proxy02-repository.jboss.org'

servers = [p1, p2]

def listFD(url):
    page = requests.get(url).text
    #print page
    soup = BeautifulSoup(page, 'html.parser')
    return [node.get('href') for node in soup.find_all('a')]

for file in listFD("https://%s/%s/%s" % (master, url, path)):
    print "Synching file: %s" % file
    try:
        o = urlparse(file)
        print "o.path: %s" % o.path
        path = o.path
        for server in servers:
            newUrl = "https://%s/%s" % (server, path)
            response = urllib2.urlopen(newUrl)
            content = response.read()
            print "%s Length: %s" % (server, len(content))
            # just throw it away
    except:
        pass
