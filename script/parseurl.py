#coding=utf-8
#python 3 version:

import sys, urllib.request, re
import json
print(123123123)
url = "http://www.wikidata.org/entity/Q712226"
wp = urllib.request.urlopen(url)
content = wp.read().decode('utf-8')
data = json.loads(content)#[0]#[0]["labels"]["en"]["value"]
match = data
print(data)