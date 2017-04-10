from ..DBHelper.dbhelper import Dbhelper
from ..utilities.commonFunctions import Utility
from flask import session,render_template

def getListOfJobs(colectn,query,li):
	output = []
	if colectn in li:
		result = Utility.getList(colectn,query)
		for res in result:
				output.append({"div":res['div'],"url":res['url'],"date":Utility.ISODateToString(res["date"])})
	return output


def getAll(query,li):
	allJobsLists={}
	for colectn in li:
		allJobsLists[colectn] = getListOfJobs(colectn,query,li)
	return allJobsLists

def getRecentJobs(li):
	allJobsLists={}
	for cmpny in li:
		collection = Dbhelper.getCollectionName(cmpny)
		result = collection.find().limit(1)
		for res in result:
		    date = res['date']
		allJobsLists[cmpny] = getListOfJobs(cmpny,{"date":date},session['lis'])
	return allJobsLists


class JobsModel:

	__startDate = ""
	__endDate = ""
	__cmpnyName = ""
	allCmnyList=['Goldmansach','Taleo','Pepsico','American Express','Kronos','Hike','Nestle']

	def __init__(self,startDate,endDate,cmpnyName):
		if startDate and endDate:
			self.__startDate = Utility.StringToISODate(startDate)
			self.__endDate = Utility.StringToISODate(endDate)
		if cmpnyName:
			self.__cmpnyName = cmpnyName



	def datecmnywiseJob(self):
		output = getListOfJobs(self.__cmpnyName, Dbhelper.getDateQuery(self.__startDate,self.__endDate),session['lis'])
		return render_template("index.html",dict={self.__cmpnyName:output},selectedList=session['lis'],list=JobsModel.allCmnyList)

	def datewiseJob(self):
		output = getAll(Dbhelper.getDateQuery(self.__startDate, self.__endDate),session['lis'])
		return render_template("index.html",dict=output,selectedList=session['lis'],list=JobsModel.allCmnyList)

	def cmnywiseJob(self):
		output = getListOfJobs(self.__cmpnyName, {},session['lis'])
		return render_template("index.html",dict={self.__cmpnyName:output},selectedList=session['lis'],list=JobsModel.allCmnyList)
