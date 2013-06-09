#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#apt-get install python-socksipy
#apt-get install python-pyspatialite

import socks, socket, urllib2, re
from pyspatialite import dbapi2 as sqlite3

site_ref = "http://exemple.com/" # <-- change this

conn = sqlite3.connect('site_map.db')
c = conn.cursor()
c.execute("CREATE TABLE if not exists todo ( url varchar(250) PRIMARY KEY, etat tinyint(1) DEFAULT 0, find_date DATETIME NULL);")
c.execute("CREATE TABLE if not exists map ( id INTEGER PRIMARY KEY AUTOINCREMENT, url_from varchar(250) DEFAULT NULL, url_to varchar(250) DEFAULT NULL);")
c.execute("CREATE TABLE if not exists pages ( url varchar(250) PRIMARY KEY, etat tinyint(1) DEFAULT 0 );")
c.execute("INSERT OR IGNORE INTO todo ( url, etat) VALUES ('"+site_ref+"', 0);")
conn.commit()

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050) # <-- change this
# 127.0.0.1:9050 = proxy Tor

socket.socket = socks.socksocket
headers = { 'User-Agent' : '-' }


c.execute("SELECT url FROM todo WHERE etat=0 ORDER BY find_date LIMIT 1;")
a= c.fetchone()

while a:
    site_ref = a[0]
    print "Scan "+site_ref
    try:
        req = urllib2.Request(site_ref, None, headers)
        htmlSource = urllib2.urlopen(req).read()
    except:
        print "HS "+site_ref
        htmlSource=""
        pass


    if htmlSource != "":
        site=site_ref
        if site_ref[-1:]!="/":
            if site_ref[7:].find('/') >0:
                site = site_ref[0:site_ref[7:].find('/')+8]
            else:
                site+="/"

        linksList = re.findall("<a.*?href=('.*?'|\".*?\").*?>.*?</a>",htmlSource)

        for link in linksList:
            try:
                if link[1:5] == 'http':
                    link = link[1:-1]
                elif link[1:2] == '/':
                    link = site+link[2:-1]
                elif link[1:3] == './':
                    link = site+link[3:-1]
                else:
                    link = site+link[1:-1]

                if link[4:].find('http')>0:
                    link=link[4+link[4:].find('http'):]
                    if link.find('&')>0:
                        link=link[0:link.find('&')]
            except:
                link = site
                pass

            if link != site:
                if link.find('out.cgi') == -1 and link.find('javascript') == -1:
                    try:
                        if link.find("'") > 4:
                            link=link[0:link.find("'")]

                        if link.find("'") != 0:
                            link=link[link.find("'"):]

                        if link.find('"') > 4:
                            link=link[0:link.find('"')]

                        if link.find('"') != 0:
                            link=link[link.find('"'):]


                        if link != "" and len(link) > 7:
                            if link[0:len(site)] == site or link.replace("www.","")[0:len(site.replace("www.",""))] == site.replace("www.",""):
                                c.execute("INSERT OR IGNORE INTO pages ( url, etat) VALUES ('"+link+"', 0);")
                            else:
                                c.execute("INSERT OR IGNORE INTO todo ( url, etat, find_date) VALUES ('"+link+"', 0, datetime('now'));")
                                c.execute("INSERT OR IGNORE INTO map ( url_from, url_to) VALUES ('"+site+"','"+link+"');")
                    except:
                        pass

    c.execute("UPDATE todo SET etat=1 WHERE url='"+site_ref+"';")
    conn.commit()
    c.execute("SELECT url FROM todo WHERE etat=0 ORDER BY find_date LIMIT 1;")
    a= c.fetchone()

conn.close()
