
# coding: utf-8

# In[1]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
furl=[]
count=0
wiki = 'http://www.futuregroup.in/careers/current-opportunities.aspx'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page,'html.parser')
import re
soup=str(soup)


# In[2]:

floc=re.findall('<div class="full_width jobtxt"><b>Location : </b>(.*?)</div><div class="full_width jobtxt">',soup)
ftitle=re.findall('<h3>(.*?)</h3><div class="key-txt jst"',soup)
url=re.findall('href="(.*?)">Apply Now',soup)


# In[3]:

for i in url:
    i='http://www.futuregroup.in/careers/'+i
    furl.append(i)
    count=count+1


# In[4]:

ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.futuregroup
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})

