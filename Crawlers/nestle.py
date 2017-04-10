
# coding: utf-8

# In[12]:




# In[27]:




# In[168]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
dates=[]
title=[]
wiki='https://tas-nestle.taleo.net/careersection/feed/joblist.rss?lang=en&portal=2170452333&searchtype=3&f=null&LOCATION=8270452333&s=1|D&a=null&multiline=true'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page,'html.parser')


# In[169]:

import re
soup1=soup
soup=str(soup)
alldates=re.findall("<pubdate>(.*?)</pubdate>",soup)
alltitles=re.findall("<item><title>(.*?)</title>",soup)
alllinks=re.findall("<link>(.*?)</link>",soup)
alllinks=alllinks[1:]
import pandas as pd
alldates=pd.to_datetime(alldates)
output = pd.DataFrame({ 'div' : alltitles, 'date': alldates })

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.nestle
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i],"date":output['date'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['date'][i],"url":alllinks[i]})


