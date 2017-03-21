
# coding: utf-8

# In[2]:




# In[171]:
import datetime
import urllib2
import json
dates=[]
titles=[]
from bs4 import BeautifulSoup
wiki = "http://www.goldmansachs.com/a/data/jobs/india.html"
page=urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
scripts=soup.find_all("tr")
z=soup.find_all("caption")
z=str(z)
a=z.find("counter")
z=z[a+9:]
b=z.find('j')
z=z[:b-1]
for i in range(2,int(z)+2):
    title=scripts[i].find_all('a')
    title=str(title)
    f=title.find('>')
    title=title[f+1:]
    g=title.find('<')
    title=title[:g]
    titles.append(title)
    date=scripts[i].find_all('td')
    fdate=date[2]
    fdate=str(fdate)
    i=fdate.find('>')
    fdate=fdate[i+1:]
    j=fdate.find('<')
    fdate=fdate[:j]
    dates.append(fdate)


# In[172]:

import pandas as pd
output = pd.DataFrame({ 'div' : titles, 'dates': dates })


# In[173]:

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
collection=db.goldmansach
for i in range(output.shape[0]):
    if collection.find({"div":output['div'][i]}).count()==0:
        collection.insert_one({"div":output['div'][i],"date":output['dates'][i]})


