from flask import Blueprint, Flask,request, render_template, redirect,url_for,session,current_app as app
from ..DBHelper.dbhelper import sqlDbhelper
from werkzeug import secure_filename

import json
import time
import os

listingQues = Blueprint('assessment',__name__,template_folder='templates')

@listingQues.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@listingQues.route('/listQuestions')
def listQuestions():
    results=sqlDbhelper.getData("select * from quesBank limit 44")
    return render_template("assessmentIndex.html",questions=results)


@listingQues.route('/ajaxUpdate',methods=['POST'])
def ajaxRecieve():
    quesId=request.json['quesId']
    ques=request.json['question']
    ans=request.json['correctAnswer']
    lev=request.json['level']
    quesType=request.json['questionType']
    skill=request.json['skillType']
    tag=request.json['tags']
    options =request.json['options']

    sqlDbhelper.updateQuery(quesId,ques,ans,lev,quesType,skill,tag,options)
    return json.dumps({'status':'OK'})

@listingQues.route('/ajaxDelete',methods=['POST'])
def ajaxDelete():
    quesId=request.json['quesId']
    #print(quesId)

    sqlDbhelper.deleteQuery(quesId)
    return redirect(url_for('assessment.listQuestions'))

@listingQues.route('/upload', methods = ['GET', 'POST'])
def upload():
   # user=Dbhelper.findOne({"email":session['email']})
   # result=user['fileInfo']
   # output=[]
   # for res in result:
   #    output.append({"File ID":res["fileId"],"File name":res["filename"],"File status":res["status"],"Date":(res['date']).strftime("%Y-%m-%d %H:%M:%S")})
   results=sqlDbhelper.getData("select * from quesBank limit 44")

   if request.method == 'POST':
      f = request.files['file']
      if f:
        filename = secure_filename(f.filename)
        if '.' in filename and filename.split('.')[1]=='csv':
          fileId=filename.split('.')[0]+str(int(time.time()*1000))+'.'+filename.split('.')[1]
          #app.config['UPLOAD_FOLDER'] = 'uploadedCSV/'
          #f.save(filename)
          f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
          #parseCsvFile.delay(fileId,filename,session['email'])
          return render_template("assessmentIndex.html",questions=results,message="File parsing is on process")
        else:
          return render_template("assessmentIndex.html",questions=results,message="File should have extension(.csv)")
      else:
        return render_template("assessmentIndex.html",questions=results,message="Choose file to upload")
   else:
      return render_template("assessmentIndex.html",questions=results)
