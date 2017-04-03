
# coding: utf-8

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
output = pd.DataFrame({ 'div' : alltitles, 'date': alldates })


# In[171]:

import datetime
from datetime import date
now = datetime.datetime.now()
output['date']=output['date'].str.split()    


# In[172]:

def Tix_label(s):
    s[2]=now.month
    s[0]=s[3]
    t=s[1]
    s[1]=s[2]
    s[2]=t
    s=str(s[0])+str(s[1])+str(s[2])
    st = datetime.datetime.strptime(s, "%Y%m%d")
    s = datetime.datetime(st.year,st.month,st.day,0,0,0,0)
    return s

output["date"] = output.loc[:,"date"].apply(Tix_label)    


# In[173]:

output



# In[174]:

#output=output[output['dates']==date.today()]


# In[175]:

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.taleo
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i],"date":output['date'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['date'][i],"url":alllinks[i]})


