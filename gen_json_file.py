#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from pyspatialite import dbapi2 as sqlite3
conn = sqlite3.connect('site_map.db')
c = conn.cursor()
c.execute("SELECT url_from FROM map group by url_from;")
listes=c.fetchall()


sites_file = open('sites.js','w')
sites_file.write("var sites = {\n  nodes:[\n")

sites_tab=[]
nb_site=0
for i in listes:
    s=i[0]
    if s[8:].find('/') >0:
        s=s[:s[8:].find('/')+8]

    if not s in sites_tab:
        sites_tab.append(s)
        nb_site+=1
        sites_file.write("\n{nodeName:'"+s+"', group:1},")


c.execute("SELECT url_to FROM map WHERE url_to NOT IN (SELECT m.url_from FROM map as m group by m.url_from) group by url_to;")
listes=c.fetchall()
for i in listes:
    s=i[0]
    if s[8:].find('/') >0:
        s=s[:s[8:].find('/')+8]

    if not s in sites_tab:
        sites_tab.append(s)
        nb_site+=1
        sites_file.write("\n{nodeName:'"+s+"', group:1},")


print str(nb_site)+" sites"

sites_file.write("\n  ],")
sites_file.write("\n /* "+str(nb_site)+" sites */")
sites_file.write("\n  links:[")


c.execute("SELECT * FROM map;")
listes=c.fetchall()
conn.close()
links={}
for i in listes:
    s=i[1]
    if s[8:].find('/')>0:
        s=s[:s[8:].find('/')+8]

    t=i[2]
    if t[8:].find('/')>0:
        t=t[:t[8:].find('/')+8]

    if not s+"#"+t in links:
        links[s+"#"+t]=1
    else:
        links[s+"#"+t]+=1

nb_site=0
for i in links:
    if links[i] >0:
        nb_site+=1
        sites_file.write("\n    {source:"+str(sites_tab.index(i[0:i.index('#')]))+", target:"+str(sites_tab.index(i[i.index('#')+1:]))+", value:"+str(links[i])+"},")

print str(nb_site)+" liens"

sites_file.write("\n  ]")
sites_file.write("\n};")
sites_file.write("\n /* "+str(nb_site)+" liens */")
sites_file.close()

