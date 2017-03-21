from flask import Flask, jsonify, json , send_file , request , render_template
from pymongo import MongoClient
import datetime


app = Flask(__name__) 
client = MongoClient('localhost')
db = client.mydb

def getDateQuery(st,end):
	query = {'date':{
					'$gte':st,
					'$lte':end
					}}
	return query


def getCollectionName(cmpnyName):
	return {
		  'Goldmansach': db.goldmansach,
		  'kronos': db.kronos,
		  'American Express':db.americanexp,
		  'pepsico':db.pepsicoJob
	}.get(cmpnyName,"")


def getUrlParameter(param):
	return request.args.get(param)

def getDate(dat):
	da=datetime.datetime.strptime(str(dat),"%Y-%m-%d %H:%M:%S")
	return str(da.day)+"-"+da.strftime("%b")+"-"+str(da.year)

def getListOfJobs(collection , query):
	result = collection.find(query)
	output=[]
	for res in result:
		output.append({"div":res['div'],"date":getDate(res["date"])})
	return output


def getAll(query):
	allJobsLists = {
					'Goldmansach' : getListOfJobs(getCollectionName('Goldmansach'),query),
					'American Express' : getListOfJobs(getCollectionName('American Express'), query),
					'Pepsico' : getListOfJobs(getCollectionName('pepsico'), query)
					}
	return allJobsLists


@app.route('/')
def listJobs():
	
	cmpnyName = getUrlParameter('company_name')	
	startDate = getUrlParameter('start_date')
	endDate = getUrlParameter('end_date')
	
	if startDate and endDate:
		st = datetime.datetime.strptime(startDate, "%Y-%m-%d")
		en = datetime.datetime.strptime(endDate, "%Y-%m-%d")

		start = datetime.datetime(st.year,st.month,st.day,0,0,0,0)
		end   = datetime.datetime(en.year,en.month,en.day,0,0,0,0)

	collection = getCollectionName(cmpnyName)

	if collection == "":
	   if startDate and endDate:
		output = getAll(getDateQuery(start, end))
	   else:
		output = getAll({}) 
		
	   return render_template("index.html",dict=output)

	elif collection and startDate and endDate:
		output = getListOfJobs(collection, getDateQuery(start, end))

	else:
		output = getListOfJobs(collection, {})

	return render_template("index.html",list=output,name=cmpnyName)


if __name__ == '__main__': 
		app.run(debug = True)



























