from flask import render_template, Blueprint,request,redirect,url_for,session
from pymongo import MongoClient
from ..utilities.commonFunctions import Utility
from ..DBHelper.dbhelper import Dbhelper

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from random import randint

users = Blueprint('users', __name__, template_folder='templates')

def sendMail(fromaddr,password,toaddr,body):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Login Credential"

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(fromaddr,password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def getListOfUser(product):
	result = Utility.getList('User', {"role":"user", "products":{"$in":[product]}})
	listOfUser = []
	for res in result:
		listOfUser.append({"name":res['name'],"email":res['email'],"products":res['products']})

	return listOfUser

@users.route('/')
def index():
	return render_template('login.html')

@users.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = Utility.getPostParameter('email')
		password = Utility.getPostParameter('password')
		session['email'] = email
		user = Dbhelper.findOne('User', { "email":email, "password":password })
		if user:
			role = user['role']
			if role == "admin":
				return redirect(url_for('users.admin'))
			elif role == "user":
				if 'permission' in user.keys():
					session['lis'] = user.get('permission').get('crawler')
				else:
					session['lis']=[]

				if session['lis']:
				   return redirect(url_for('jobListing.jobListing'))
				else:   
				   return render_template('companiesPopUp.html')
		else:
			return render_template('login.html',message="Enter valid credential")
			
@users.route('/admin')
def admin():
	if Utility.isLoggedIn():
		result = Dbhelper.findOne('User' , {"email":session['email']})
		listOfProducts = result['products']
		dic = {}
		for product in listOfProducts:
			dic[product] = getListOfUser(product)
		return render_template('admin.html',dict=dic)
	return redirect(url_for('users.index'))


@users.route('/logout')
def logout():
	session.clear()
	return render_template('login.html',logoutMessage="You have successfully logged out")
			
@users.route('/register')
def register():
	return render_template('register.html')

@users.route('/registerSuccess')
def registerSucess():
	if Utility.isLoggedIn():
		name=Utility.getUrlParameter('name')
		email=Utility.getUrlParameter('email')
		product=Utility.getUrlParameterList('products')
		passwd=randint(1000,523253555)
		if not Dbhelper.findOne('User',{"email":email}):
			Dbhelper.insert('User' , { "name":name,"email":email,"products":product,"password":str(passwd),"role":"user" })
			body="User Name:  "+name+'\n'+"Password:   "+str(passwd)
			sendMail("mohit.mittal@iimjobs.com","123456789!@",email,body)
			return redirect(url_for('users.admin'))
		else:
			return render_template('register.html',message="Emailid is already registered")	
	return redirect(url_for('users.index'))	

@users.route('/admin/delete/<emailId>')
def delete(emailId):
	if Utility.isLoggedIn():
		Dbhelper.delete('User', "email", emailId)
		return redirect(url_for('users.admin'))

@users.route('/user/selectCompanies')
def selectCompanies():
	if Utility.isLoggedIn():
		listOfCompanies = Utility.getUrlParameterList('companies')
		collection=Dbhelper.getCollectionName('User')
		collection.update({"email":session['email']},{"$set":{"permission":{"crawler":listOfCompanies}}})
		session['lis'] = listOfCompanies;
		return redirect(url_for('jobListing.jobListing'))		
	
    

		