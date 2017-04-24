
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
		if oldPassword and newPassword:
			collection.update({"email":session['email'],"password":oldPassword},{"$set":{"password":newPassword}})

		return redirect(url_for('jobListing.logout'))

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
