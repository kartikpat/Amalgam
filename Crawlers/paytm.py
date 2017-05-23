
# coding: utf-8

# In[14]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
ftitle=[]
fdate=[]
floc=[]
fur=[]
furl=[]
wiki = 'https://jobs.lever.co/paytm'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
import re
soup=str(soup)
    


# In[15]:

alldata=re.findall('<a class="posting-title" href="(.*?)"><h5>(.*?)</h5><div class="posting-categories"><span class="sort-by-location posting-category small-category-label" href="#">(.*?)</span>',soup)


# In[16]:

count=0
for i in alldata:
    furl.append(i[0])
    ftitle.append(i[1])
    floc.append(i[2])
    count=count+1


# In[17]:

ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.paytm
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})

