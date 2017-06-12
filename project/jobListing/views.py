from flask import Blueprint, Flask,request, render_template, redirect,url_for,session
from ..utilities.commonFunctions import Utility
from ..DBHelper.dbhelper import Dbhelper
from model import JobsModel
import model

listingJob = Blueprint('jobListing',__name__,template_folder='templates')

@listingJob.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@listingJob.route('/editProfile', methods = ['POST', 'GET'])
def editProfile():
    if request.method == 'POST':
        collection = Dbhelper.getCollectionName("User")
        oldPassword = Utility.getPostParameter('oldPassword')
        newPassword = Utility.getPostParameter('newPassword')
        if Dbhelper.findOne('User',{"email":session['email'],"password":oldPassword}):
            collection.update({"email":session['email'],"password":oldPassword},{"$set":{"password":newPassword}})
            return redirect(url_for('jobListing.logout'))
        else:
            output = model.getRecentJobs(session['lis'])
            return render_template('index.html',wrongPassword="Enter correct old password",dict=output,selectedList=session['lis'],list=JobsModel.allCmnyList)

@listingJob.route('/editCompanies')
def editCompanies():
    collection=Dbhelper.getCollectionName("User")
    companies=request.args.getlist('permissionCompanies')
    if companies:
        collection.update({"email":session['email']},{"$set":{"permission.crawler":companies}})
        session['lis']=companies

    return redirect(url_for('jobListing.jobListing'))

@listingJob.route('/jobListing')
def jobListing():
    if Utility.isLoggedIn():
        output = model.getRecentJobs(session['lis'])

        return render_template("index.html",dict=output,selectedList=session['lis'],list=JobsModel.allCmnyList )
    else:
        return redirect(url_for('users.index'))

@listingJob.route('/jobListing/listJob')
def listJob():

    cmpnyName = Utility.getUrlParameter('company_name')
    startDate = Utility.getUrlParameter('start_date')
    endDate = Utility.getUrlParameter('end_date')

    listOfJobs = JobsModel(startDate,endDate,cmpnyName)

    if startDate and endDate and cmpnyName:
        return listOfJobs.datecmnywiseJob()
    elif startDate and endDate:
        return listOfJobs.datewiseJob()
    elif cmpnyName:
        return listOfJobs.cmnywiseJob()
    else:
        return redirect(url_for('jobListing.jobListing'))


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

@listingJob.route('/naukri')
def jobListing1():
		output = getJobs()
		return render_template("naukri.html",dict=output )

@listingJob.route('/naukri/location')
def listJob1():
	output = getJobsByLocation()
	return render_template("index1.html",dict1=output,dict={} )
