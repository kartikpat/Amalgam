
# coding: utf-8

# In[20]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import re
ftitle=[]
fdate=[]
floc=[]
furl=[]
fur=[]
count=0
wiki = 'https://jobs.zs.com/go/Experienced-Candidates-India/1356900/'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
soup=str(soup)
alld=re.findall('<a class="jobTitle-link" href="(.*?)">(.*?)</a>\n</span>\n<div class="jobdetail-phone visible-phone visible-sm">\n<span class="jobLocation">(.*?)</span>\n<span class="jobDate">(.*?)\n\t\t\t\t\t\t\t\t\t\t\t\t\t</span>\n<span class="jobDistance">',soup)
for i in alld:
    fur.append(i[0])
    ftitle.append(i[1])
    floc.append(i[2])
    fdate.append(i[3])
for i in fur:
    i='https://jobs.zs.com'+i
    furl.append(i)
    count=count+1  
fdate=pd.to_datetime(fdate)    
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.zs
for i in range(count):
    if collection.find({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]})    

