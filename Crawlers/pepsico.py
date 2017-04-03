
# coding: utf-8

# In[4]:




# In[3]:




# In[ ]:
import datetime
import urllib2
import json
from bs4 import BeautifulSoup
import re
dates=[]
title=[]
url=[]
for i in range(1,11):
    wiki = "https://apply.pepsicojobs.com/jobs?page="+str(i)
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page,'html.parser')
    scripts=soup.find_all("script")
    string = scripts[12].text[15:-2]
    dObj = json.loads(string)
    strData = json.dumps(dObj,indent=4)
    strData1=str(strData)  
    name=[]
    for i in range(1,11):
        a=strData1.find('title')
        strData1=strData1[a-1:]
        b=strData1.find(']')
        nm=strData1[:b]
        name.append(nm)
        strData1=strData1[b:]
    name=str(name)    
    for i in range(1,11):
        a=name.find('title')
        name=name[a+9:]
        b=name.find('"')
        x=name[:b]
        title.append(x)
        name=name[b:]
    strData=str(strData)    
    for i in range(1,11):
        a=strData.find('create_date')
        date=strData[a+15:a+39]
        dates.append(date)
        strData=strData[a+39:]
    soup1=str(soup)
    z=re.findall('"job_url":"(.*?)"',soup1)
    url.append(z)
furl=[]
for j in range(0,10):
    for u in url[j]:
        furl.append(u)

# In[ ]:

import pandas as pd


# In[ ]:

output = pd.DataFrame({ 'div' : title, 'dates': dates })


# In[ ]:

output['dates']=output['dates'].str.extract('(\d\d\d\d+-\d\d+-\d\d)')

# In[ ]:



# In[ ]:
from datetime import date
def Tix_label(s):
    st = datetime.datetime.strptime(s, "%Y-%m-%d")
    s = datetime.datetime(st.year,st.month,st.day,0,0,0,0)
    return s
output["dates"] = output.loc[:,"dates"].apply(Tix_label)      
#output=output[output['dates']==date.today()]  


# In[ ]:

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db= client.mydb
collection=db.pepsico
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['dates'][i],"url":furl[i]})


# In[13]:

collection.find()



# In[4]:

output


