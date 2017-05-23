
# coding: utf-8

# In[40]:

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

display = Display(visible=0, size=(800, 600))
display.start()
from pymongo import MongoClient
import datetime
import time
import os
import pandas as pd
count=0
ftitle=[]
floc=[]
fdate=[]
furl=[]
fur=[]
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser= webdriver.Chrome(chromedriver)

browser.implicitly_wait(5)

url="http://careers.teamhgs.com/#/career"
browser.get(url)


# In[41]:

html=browser.page_source.encode("utf-8")


# In[42]:

import re
alld=re.findall('class="ng-binding" href="#(.*?)">(.*?)</a> </h3>\n                                    <h5> \xc2\xa0Job Code :  <span class="ng-binding">(.*?)</span> \n                                           \xc2\xa0\n                                      Number Of Positions :  <span class="ng-binding"> (.*?) </span> \n                                    </h5>\n                                    <ul class="result-list-ul job-details">\n                                        <!--                               <li> <i class="fa fa-briefcase"></i>&nbsp;{{jobData.ExpRange}}&nbsp;<span>yrs</span></li>-->\n                                        <li class="ng-binding"> <i class="fa fa-briefcase"></i>\xc2\xa0(.*?)\xc2\xa0</li>\n                                        <li class="ng-binding"> <i class="fa fa-map-marker"></i>\xc2\xa0 (.*?)</li>\n(.*?)',html)
fdate=re.findall('class="post_date ng-binding"> Posted on (.*?) </span>\n ',html)


# In[43]:

for i in alld:
    ftitle.append(i[1])
    fur.append(i[0])
    floc.append(i[5]) 
    count=count+1
for i in fur:
        i="http://careers.teamhgs.com/#"+i
        furl.append(i)
fdate=pd.to_datetime(fdate)


# In[49]:

client=MongoClient('localhost',27017)
db= client.mydb
collection=db.hindujaglobal
for i in range(count):
    if collection.find({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]}).count()==0:
        collection.insert_one({"div":ftitle[i],"date":fdate[i],"url":furl[i],'location':floc[i]})

