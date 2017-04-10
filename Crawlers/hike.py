
# coding: utf-8

# In[20]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
ftitle=[]
floc=[]
furl=[]
count=0
wiki = 'http://careers.hike.in/postings.php'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page,'html.parser')
import re
soup=str(soup)
values=re.findall('<div class="team"><a href="(.*?)" target="_blank">(.*?)</a><span class="location"><i class="fa fa-map-marker"></i>(.*?)<span>',soup)
for i in values:
    ftitle.append(i[1])
    furl.append(i[0])
    floc.append(i[2]) 
    count=count+1
ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.hike
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})



