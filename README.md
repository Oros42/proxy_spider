proxy_spider
============

Cartographie de sites web en passant par un proxy comme Tor. 

Exemple de carte généré : https://raw.github.com/Oros42/proxy_spider/master/network.png

Notes
=====
proxy_spider ne parcours que les liens qui pointent sur d'autres sites.  
Il ne parcourt pas les liens d'un même site.


Étape 1
=======

```bash
apt-get install python-socksipy
apt-get install python-pyspatialite
```


Étape 2
=======

Dans proxy_spider.py, il faut modifier : 
la ligne 10 : 
```python
site_ref = "http://exemple.com/" # <-- change this
```
et la ligne 20 :
```python
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050) # <-- change this
# 127.0.0.1:9050 = proxy Tor
```


Étape 3
=======

Lancer proxy_spider.py qui va parcourir les sites : 
```bash
python proxy_spider.py > log.txt &
```


Étape 4
=======

Lorsqu’il y a suffisamment de site de parcourus, lancer gen_json_file.py pour créer la carte : 
```bash
python gen_json_file.py
```


Étape 5
=======

Ouvrir map.html avec un navigateur web. 

