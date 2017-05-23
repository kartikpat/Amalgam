
# coding: utf-8

# In[9]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
ftitle=[]
fdate=[]
floc=[]
furl=[]
wiki = 'https://westernun.referrals.selectminds.com/jobs/search/2037004'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
import re
soup=str(soup)


# In[10]:

alldata=re.findall('<a class="job_link font_bold" href="(.*?)">(.*?)</a></p>\n<p class="jlr_cat_loc">\n<span class="font_bold">Location:</span>\n<span class="location">\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t</span>\n</p>\n<p class="jlr_cat_loc">\n<span class="font_bold">Category:</span>\n<span class="category">(.*?)</span>\n</p>\n</div>\n',soup)


# In[11]:

count=0
for i in alldata:
    furl.append(i[0])
    ftitle.append(i[1])
    floc.append(i[2])
    count=count+1


# In[12]:

ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.westernunion
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i]})

