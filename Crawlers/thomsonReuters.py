
# coding: utf-8

# In[1]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
ftitle=[]
floc=[]
furl=[]
fur=[]
count=0
for i in range(1,5):
    wiki = 'http://jobs.thomsonreuters.com/ListJobs/All/Search/tr-full-country-name/india/Page-'+str(i)
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page,'html.parser')
    import re
    soup=str(soup)
    alldata=re.findall('<td class="coloriginaljobtitle">\n<a href="(.*?)">(.*?)</a>\n</td>\n<td class="colcity">\r\n(.*?)                    </td>',soup)
    for i in alldata:
        fur.append(i[0])
        ftitle.append(i[1])
        floc.append(i[2])
        count=count+1
for i in fur:
        i="http://jobs.thomsonreuters.com"+i
        furl.append(i)  
ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.thomson
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})

