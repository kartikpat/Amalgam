
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
for i in range(0,2):
    wiki = 'http://www.landmarkgroup.com/careers/job-listing.php?pg='+str(i)+'#tab02'
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    import re
    soup=str(soup)
    alldata=re.findall('<div class="job-title">\n<div class="post">\n<a href="(.*?)" target="_blank" title="(.*?)">(.*?)</a>\n</div>\n<div class="division">(.*?)</div>\n</div>\n<div class="type">\n<div>(.*?)</div>\n</div>\n<div class="location">\n<td width="75%">(.*?)\n',soup)
    count=0
    for i in alldata:
        furl.append(i[0])
        ftitle.append(i[1])
        floc.append(i[5])
        count=count+1
    ti= datetime.date.today()
    date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
    date=pd.to_datetime(date)
    client=MongoClient('localhost',27017)
    db= client.mydb
    collection=db.landmarkgroup
    for i in range(count):
        if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
            collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})

