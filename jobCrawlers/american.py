
# coding: utf-8

# In[7]:




# In[1]:
import datetime
import urllib2
import json
dates=[]
title=[]
from bs4 import BeautifulSoup
for i in range(1,4):
    wiki = "https://jobs.americanexpress.com/india/jobs?page="+str(i)
    page=urllib2.urlopen(wiki)
    soup = BeautifulSoup(page,'html.parser')
    scripts=soup.find_all("script")
    string = scripts[11].text[15:-2]
    dObj = json.loads(string)
    strData = json.dumps(dObj,indent=4)
    strData1=str(strData)
    strData=str(strData)
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
    for i in range(1,11):
        a=strData.find('create_date')
        date=strData[a+15:a+40]
        dates.append(date)
        strData=strData[a+40:]


# In[2]:
from datetime import date
import pandas as pd
output = pd.DataFrame({ 'div' : title, 'dates': dates })
output['dates']=output['dates'].str.extract('(\d\d\d\d+-\d\d+-\d\d)')
# In[5]:

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
collection=db.americanexp
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['dates'][i]})


# In[13]:

collection.find()


# In[8]:

date.today()


# In[9]:

output

