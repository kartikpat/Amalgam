
# coding: utf-8

# In[12]:

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
wiki = 'https://careers.societegenerale.com/Search/job-offers-search-results?searchType=1&search_continent%5B%5D=%2FLOCATIONS%2FASIA__ASIA_PAC&search_country%5B%5D=%2FLOCATIONS%2FASIA__ASIA_PAC%2FINDIA&search_continent_fake=&search_country_fake=&search_region_fake=&search_department_fake=&search_job%5B%5D=&search_entity%5B%5D=&search_date=%2FDATEJOB%2FPAST_WEEK&search_keyword=Enter+key+words'
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
import re
soup=str(soup)
    


# In[13]:

alldata=re.findall(' title="(.*?)" type="checkbox"/></td>\n<th scope="row">(.*?)</th>\n<td><a href="(.*?)">(.*?)</a></td>\n<td>(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)</td>\n</tr>',soup)


# In[14]:

count=0
for i in alldata:
    ftitle.append(i[0])
    fdate.append(i[1])
    fur.append(i[2])
    floc.append(i[7])
    count=count+1


# In[15]:

for i in fur:
    i='https://careers.societegenerale.com'+str(i)
    furl.append(i)


# In[16]:

fdate=pd.to_datetime(fdate)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.SocieteG
for i in range(count):
    if collection.find({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]})



