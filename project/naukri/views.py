
from flask import Blueprint, Flask,request, render_template, redirect,url_for,session
from ..utilities.commonFunctions import Utility
from ..DBHelper.dbhelper import Dbhelper



naukri = Blueprint('naukri',__name__,template_folder='templates')

def getJobs():
	allJobsLists = {}
	result = Dbhelper.getCollectionName("Naukri").aggregate([{ "$group" : { "_id" : "$organization","jobs": { "$push" : "$$ROOT"}}}])
	for res in result:
		output = []
		for job in res['jobs']:
			output.append({"title":job['title'],"location":job['location'],"date":Utility.ISODateToString(job['date'])})
		allJobsLists[res['_id']] = output
	return allJobsLists

def getJobsByLocation():
	allJobsLists = {}
	result = Dbhelper.getCollectionName("Naukri").aggregate([{ "$group" : { "_id" : "$location[1]","jobs": { "$push" : "$$ROOT"}}}])
	for res in result:
		output = []
		for job in res['jobs']:
			output.append({"title":job['title'],"date":Utility.ISODateToString(job['date'])})
		allJobsLists[res['_id']] = output
	return allJobsLists

@naukri.route('/jobListings')
def jobListing():
		output = getJobsByLocation()
		return render_template("index1.html",dict=output )

@naukri.route('/jobListings/location')
def listJob():
	output = getJobsByLocation()
	return render_template("index1.html",dict1=output,dict={} )
