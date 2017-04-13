
# coding: utf-8

# In[11]:




# In[16]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
job_ls=['Information-Technology-jobs','Management-Consulting-jobs','Accounting-Auditing-jobs','Communications-and-Public-Relations-jobs','Tax-jobs']
ftitle=[]
fdate=[]
floc=[]
furl=[]
for i in range(0,5):
    wiki = 'https://jobs2.deloitte.com/in/en/'+job_ls[i]
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    import re
    soup=str(soup)
    jobtitle=re.findall('<div class="job-title"><span itemprop="title">(.*?)</span></div>',soup)
    jobdate=re.findall('<span class="job-post-date" data-posteddate="(.*?)">',soup)
    joblocation=re.findall('<span class="job-loacation" itemprop="jobLocation">(.*?)</span>',soup)
    joburl=re.findall('href="(/in/en/job/.*?)"',soup)
    ftitle.append(jobtitle)
    fdate.append(jobdate)
    floc.append(joblocation)
    furl.append(joburl)

# In[26]:

finloc=[]
findate=[]
fintitle=[]
finlink=[]
count=0
for j in range(0,5):
    for i in floc[j]:
        finloc.append(i)
        count=count+1
for j in range(0,5):
    for i in fdate[j]:
        findate.append(i)  
for j in range(0,5):
    for i in ftitle[j]:
        fintitle.append(i)
for j in range(0,5):
    for i in furl[j]:
        i='https://jobs2.deloitte.com'+i
        finlink.append(i)        


# In[34]:
import pandas as pd
findate=pd.to_datetime(findate)


# In[37]:

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.deloitte
for i in range(count):
    if collection.find({"div":fintitle[i],"date":findate[i],"location":finloc[i],"url":finlink[i]}).count()==0:
        collection.insert_one({"div":fintitle[i],"date":findate[i],"location":finloc[i],"url":finlink[i]})


