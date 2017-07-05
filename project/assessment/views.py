from flask import Blueprint, Flask,request, render_template, redirect,url_for,session,current_app as app
from ..DBHelper.dbhelper import sqlDbhelper
from werkzeug import secure_filename
from project.tasks import parseCsvFile ,updateDataElastic,deleteDataElastic
from ..utilities.commonFunctions import Utility
from ..DBHelper.dbhelper import Dbhelper
import datetime
import model
import json
import time
import os
import requests

listingQues = Blueprint('assessment',__name__,template_folder='templates')

@listingQues.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@listingQues.route('/listQuestions')
def listQuestions():
    dbObj=sqlDbhelper()
    results=dbObj.getData("select * from quesBank;")
    user=Dbhelper.findOne('User',{"email":"mohit.mittal@iimjobs.com"})
    uploadedFiles=user.get('permission').get('Assessment').get('uploadedCSV',None)
    return render_template("assessmentIndex.html",questions=results,files=uploadedFiles)


@listingQues.route('/ajaxUpdate',methods=['POST'])
def ajaxUpdate():
    quesId=request.json['quesId']
    ques=request.json['question']
    ans=request.json['correctAnswer']
    lev=request.json['level']
    quesType=request.json['questionType']
    skill=request.json['skillType']
    tag=request.json['tags']
    options =request.json['options']

    # print(request.json)
    dbObj=sqlDbhelper()
    dbObj.updateQuery(quesId,ques,ans,lev,quesType,skill,tag,options)
   
    # updateDataElastic.delay(request.json)
    return json.dumps({'status':'OK'})

@listingQues.route('/ajaxDelete',methods=['POST'])
def ajaxDelete():
    quesId=request.json['quesId']
    dbObj=sqlDbhelper()
    dbObj.deleteQuery(quesId)

    deleteDataElastic.delay([quesId])
    return json.dumps({'status':'OK'})

@listingQues.route('/ajaxDeleteMultiple',methods=['POST'])
def ajaxDeleteMultiple():
    quesIdArr=request.json['id']
    # print(quesIdArr)
    dbObj=sqlDbhelper()
    for id in quesIdArr:
         dbObj.deleteQuery(id)

    deleteDataElastic.delay(quesIdArr)     
    return json.dumps({'status':'OK'})   

@listingQues.route('/ajaxSetLevelMultiple',methods=['POST'])
def ajaxSetLevelMultiple():
  quesIds=request.json['ids']
  lev=request.json['level']

  dbObj=sqlDbhelper()
  for id in quesIds:
    dbObj.updateLevel(id,lev)
    
  return json.dumps({'status':'OK'})

@listingQues.route('/ajaxSetQuesTypeMultiple',methods=['POST'])
def ajaxSetQuesTypeMultiple():
  quesIds=request.json['ids']
  quesType=request.json['quesType']
  
  dbObj=sqlDbhelper()
  for id in quesIds:
    dbObj.updateQuestionType(id,quesType)

  return json.dumps({'status':'OK'})

@listingQues.route('/ajaxSetSkillTypeMultiple',methods=['POST'])
def ajaxSetSkillTypeMultiple():
  quesIds=request.json['ids']
  skillType=request.json['skillType']
  
  dbObj=sqlDbhelper()
  for id in quesIds:
    dbObj.updateskillType(id,skillType)

  return json.dumps({'status':'OK'})  


def elasticSearch(uri, term):
  """Simple Elasticsearch Query"""
  query = json.dumps({
      "query": {
          "match_phrase": {
              "_all" : term
          }
      }
  })
  response = requests.get(uri, data=query)
  results = json.loads(response.text)
  return results

@listingQues.route('/searchKeyword',methods=['GET','POST'])
def searchKeyword():
   phrase = Utility.getPostParameter('phrase')
   # phrase=request.form.get('phrase', "None")
   print(phrase)
   if phrase != None:
       li=[]
       
       results = elasticSearch('http://localhost:9200/assessment/questions/_search', phrase)
       data =  results['hits']['hits']
       i = 0
       for doc in data:
          # print(doc)
          li.append([])
          li[i].append(doc['_source']['doc']['quesId'])
          li[i].append("hello")
          li[i].append(doc['_source']['doc']['question'])
          li[i].append(doc['_source']['doc']['options'])
          li[i].append(doc['_source']['doc']['correctAnswer'])
          li[i].append(doc['_source']['doc']['level'])
          li[i].append(doc['_source']['doc']['questionType'])
          li[i].append(doc['_source']['doc']['skillType'])
          li[i].append(doc['_source']['doc']['tags'])

          i=i+1
          
       return render_template("assessmentIndex.html",questions=li)
   else:
       return redirect(url_for('assessment.listQuestions'))     
   # return json.dumps({"hello":"hii"})   

@listingQues.route('/upload', methods = ['GET', 'POST'])
def upload():
  
   dbObj=sqlDbhelper()
   results=dbObj.getData("select * from quesBank")
   # session['email']
   user=Dbhelper.findOne('User',{"email":"mohit.mittal@iimjobs.com"})
   uploadedFiles=user.get('permission').get('Assessment').get('uploadedCSV',None)

   if request.method == 'POST':
      f = request.files['file']
      if f:
        filename = secure_filename(f.filename)
        if '.' in filename and filename.split('.')[1]=='csv':
          fileId=filename.split('.')[0]+str(int(time.time()*1000))+'.'+filename.split('.')[1]
          f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileId)) 
          parseCsvFile.delay(fileId,filename,"mohit.mittal@iimjobs.com")
          #Dbhelper.arrUpdate('User',{'email':session['email']},{"permission.Assessment.uploadedCSV":{"fileName":filename,"fileId":fileId,"date":datetime.datetime.now()}},"$push")
          #app.config['UPLOAD_FOLDER'] = 'uploadedCSV/'
          #f.save(filename)
          #f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
          #parseCsvFile.delay(fileId,filename,session['email'])
          return render_template("assessmentIndex.html",questions=results,files=uploadedFiles,message="File parsing is on process")
          #return redirect(url_for('assessment.listQuestions'))
        else:
          #return redirect(url_for('assessment.listQuestions'))
           return render_template("assessmentIndex.html",questions=results,files=uploadedFiles,message="File should have extension(.csv)")
      else:
        #return redirect(url_for('assessment.listQuestions'))
         return render_template("assessmentIndex.html",questions=results,files=uploadedFiles,message="Choose file to upload")
   else:
      return redirect(url_for('assessment.listQuestions'))
       # return render_template("assessmentIndex.html",questions=results,files=uploadedFiles)
