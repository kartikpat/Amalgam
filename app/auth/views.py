from flask import  Flask,request, redirect,url_for,session, current_app, abort, make_response, jsonify
from ..utilities import isLoggedIn
from . import auth
from itsdangerous import URLSafeTimedSerializer

# from ..DBHelper.dbhelper import sqlDbhelper

@auth.route('/')
def index():
    # return make_response(jsonify({'error': 'Not found'}), 200)
    message = ''
    abort(404, {
    	'message': message,
    	'status': 'fail'
    })

# @auth.route('/')
# def index():
#     if isLoggedIn():
#         return redirectUserBasisRoleAndService()
#     else:
#         return redirect(url_for('.login'))
#
# @auth.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = Utility.getPostParameter('email')
#         password = Utility.getPostParameter('password')
#         service =Utility.getPostParameter('serviceSelect')
#
#         user = Dbhelper.findOne('User', { "email":email, "password":password ,"products":service})
#         if not email or not password or not service or not user:
#             return render_template('login.html',message="Enter valid credential and choose authorised service")
#
#         session['role'] = user['role']
#         session['email'] = email
#         session['service']=service
#
#         if session['role']=='user':
#             session['lis']=user['permission'].get(service)
#
#     if isLoggedIn():
#         return redirectUserBasisRoleAndService()
#     else:
#         return render_template('login.html')
#
# @auth.route('/register', methods = ['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#
#         # check that email is already registered or not
#         dbObj = sqlDbhelper()
#         query = "select count(*) from users where email=%s"
#         dbObj.cur.execute(query, (email, ))
#         if dbObj.cur.fetchone()[0] == 0:
#             query = "insert into user ( email) VALUES ( %s)"
#             dbObj.cur.execute(query, ( email,))
#             dbObj.sqlDb.commit()
#             dbObj.sqlDb.close()
#             token = getToken(email)
#             body="Set password using below link\n"+"http://127.0.0.1:5000/setPassword?token="+token
#             sendMail.delay(email,"Set Password",body)
#             return render_template('register.html', message = "Successfully Registered! Kindly activate your account.")
#         else:
#             return render_template('register.html', message = "Emailid is already registered")
#
#     if isLoggedIn():
#         return redirectUserBasisRoleAndService()
#     else:
#         return render_template('register.html')
#
# def redirectUserBasisRoleAndService():
#     if session["role"] == "admin":
#         return redirect(url_for('admin.loadDashboard'))
#     elif session['role'] == "user":
#         if session['service'] == 'crawler':
#             if session['listOfCompanies']:
#                 return redirect(url_for('jobListing.listJobs'))
#             else:
#                 return redirect(url_for('jobListing.selectCompanies'))
#         elif session['service']=='assessment':
#             return redirect(url_for('assessment.listQuestions'))
#
# def getToken(email):
#     ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
#     return ts.dumps(email,salt='email-confirm-key')
#
#
# def verifyToken(token):
#     s = Serializer('sdlkfdklsjfljsd')
#     try:
#         data = s.loads(token)
#     except:
#         return None
#     id = data.get('email')
#     if id:
#         return id
#     return None
