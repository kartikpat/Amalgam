import urllib2,lxml.html
from pymongo import MongoClient
import datetime


client = MongoClient("localhost",27017)
db = client.mydb
collection = db.kronos

for i in range(0,25,5):
	url="https://kronos.avature.net/careers/SearchJobs/?jobOffset="+str(i)
	file = urllib2.urlopen(url)

	data=file.read()

	file.close()

	doc=lxml.html.document_fromstring(data)

	#txt2=doc.xpath('//body/div/h1')
	txt2=doc.xpath('//ul/li/h3/a')
	#print(txt2)

	now= datetime.datetime.now()

#print(txt.text)
	for txt in txt2:
		if collection.find({"div":txt.text}).count()==0:
          		collection.insert_one({"div":txt.text,"date":datetime.datetime(now.year,now.month,now.day,0,0,0,0)})



