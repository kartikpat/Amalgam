
# coding: utf-8

# In[35]:

import datetime
import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import re
ftitle=[]
floc=[]
furl=[]
fur=[]
field=[]
descrip=[]
count=0
alldata=[]
for i in range(1,4):
    wiki='https://careers.northerntrust.com/jobs/search/862972/page'+str(i)
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page,'html.parser')
    soup=str(soup)
    alld=re.findall('<p><a class="job_link font_bold" href="(.*?)">(.*?)</a></p>\n<p class="jlr_cat_loc">\n<span class="font_bold">Location:</span>\n<span class="location">\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t</span>\n</p>\n<p class="jlr_cat_loc">\n<span class="font_bold">Category:</span>\n<span class="category">(.*?)</span>\n</p>\n</div>\n<div class="jlr_content">\n<div class="jlr_content_full">\n<p class="jlr_description">(.*?)</p>',soup)
    alldata.append(alld)
for  j in range(0,3):
    for i in alldata[j]:
        furl.append(i[0])
        ftitle.append(i[1])
        floc.append(i[2])
        field.append(i[3])
        descrip.append(i[4])    
        count=count+1
ti= datetime.date.today()
date=str(ti.year)+'/'+str(ti.month)+'/'+str(ti.day)
date=pd.to_datetime(date)
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.northerntrust
for i in range(count):
    if collection.find({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i],'field':field[i],'description':descrip[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":date,"url":furl[i],'location':floc[i],'field':field[i],'description':descrip[i]})

