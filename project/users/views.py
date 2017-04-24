from flask import render_template, Blueprint,request,redirect,url_for,session
from pymongo import MongoClient
from ..utilities.commonFunctions import Utility
from ..DBHelper.dbhelper import Dbhelper
from celery import Celery
from flask import Flask
import boto.ses
from random import randint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
users = Blueprint('users', __name__, template_folder='templates')
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

AWS_ACCESS_KEY = 'AKIAIBKUBCW3L26UNWDA'  
AWS_SECRET_KEY = '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'

connection = boto.ses.connect_to_region(
            'us-west-2',
            aws_access_key_id=AWS_ACCESS_KEY, 
            aws_secret_access_key=AWS_SECRET_KEY
        )

def getToken(mailId):
    s = Serializer('sdlkfdklsjfljsd')
    return s.dumps({'email': mailId}).decode('utf-8')

   
def verifyToken(token):
    s = Serializer('sdlkfdklsjfljsd')
    try:
        data = s.loads(token)
    except:
        return None
    id = data.get('email')
    if id:
        return id
    return None

@celery.task
def sendMail(to,subject,body):
    from_addr = 'crawler@iimjobs.com'
    return connection.send_email(from_addr,subject,None,to,format='text',text_body=body,html_body =None)

def getListOfUser(product):
    result = Utility.getList('User', {"role":"user", "products":{"$in":[product]}})
    listOfUser = []
    for res in result:
        listOfUser.append({"name":res['name'],"email":res['email'],"products":res['products']})

    return listOfUser

@users.route('/')
def index():
    if 'email' in session :
        return redirect(url_for('users.login'))
    else:    
        return render_template('login.html')

@users.route('/login', methods = ['POST', 'GET'])
def login():
        if request.method == 'POST':
            email = Utility.getPostParameter('email')
            password = Utility.getPostParameter('password')
            user = Dbhelper.findOne('User', { "email":email, "password":password })
            if not user:
                return render_template('login.html',message="Enter valid credential")

            session['role'] = user['role']
            session['email'] = email
            if 'permission' in user.keys():
                session['lis'] = user.get('permission').get('crawler')
            else:
                session['lis']=[]

        if 'email' in session:
            if session['role'] == "admin":
                return redirect(url_for('users.admin'))
            elif session['role'] == "user" and session['lis']:
                return redirect(url_for('jobListing.jobListing'))
            else:  
                return render_template('companiesPopUp.html')     
        else:    
            return render_template('login.html')           
        

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
        #passwd=randint(1000,523253555)
        if not Dbhelper.findOne('User',{"email":email}):
            Dbhelper.insert('User' , { "name":name,"email":email,"products":product,"password":"","role":"user" })
            #body="User Name:  "+name+'\n'+"Password:   "+str(passwd)
            token = getToken(mailId = email)
            body="Set password using below link\n"+"http://crawler.iimjobs.com/setPassword?token="+token
            sendMail(email,"Set Password",body)
            return redirect(url_for('users.admin'))
        else:
            return render_template('register.html',message="Emailid is already registered")
    return redirect(url_for('users.index'))

@users.route('/setPassword')
def setPassword():
    return render_template('setPassword.html')

@users.route('/setPasswordSucess')
def setPasswordSucess():
    token = request.args.get('hiddenToken')
    password= request.args.get('newPassword')
    email = verifyToken(token)
    Dbhelper.update('User',{"email":email},{"password":password})
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
