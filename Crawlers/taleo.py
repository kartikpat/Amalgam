
# coding: utf-8

# In[13]:




# In[27]:




# In[168]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
dates=[]
title=[]
wiki = "https://xl.taleo.net/careersection/feed/joblist.rss?lang=en&portal=12100010693&searchtype=3&f=null&s=3|D&a=null&multiline=true"
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page,'html.parser')


# In[169]:

import re
soup1=soup
soup=str(soup)
alldates=re.findall("<pubdate>(.*?)</pubdate>",soup)
alltitles=re.findall("<item><title>(.*?)</title>",soup)
alltitles=alltitles[0:-1]
alllinks=re.findall("<link>(.*?)</link>",soup)
alllinks=alllinks[1:-1]
# In[170]:
import pandas as pd
alldates=pd.to_datetime(alldates)
output = pd.DataFrame({ 'div' : alltitles, 'date': alldates })

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.taleo
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i],"date":output['date'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['date'][i],"url":alllinks[i]})



# In[14]:

output

