from flask import Blueprint, Flask,request, render_template, redirect,url_for,session,current_app as app
from ..DBHelper.dbhelper import sqlDbhelper
from werkzeug import secure_filename
from project.tasks import parseCsvFile
from ..utilities.commonFunctions import Utility
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
    results=sqlDbhelper.getData("select * from quesBank limit 44")
    return render_template("assessmentIndex.html",questions=results)


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
    sqlDbhelper.updateQuery(quesId,ques,ans,lev,quesType,skill,tag,options)
    # es.update(index='assessment',doc_type='questions',id=quesId,
    #             body={"doc":temp} )
    updateElastic(quesId,request.json)
    return json.dumps({'status':'OK'})

@listingQues.route('/ajaxDelete',methods=['POST'])
def ajaxDelete():
    quesId=request.json['quesId']
    #print(quesId)

    sqlDbhelper.deleteQuery(quesId)
    return json.dumps({'status':'OK'})

@listingQues.route('/ajaxDeleteMultiple',methods=['POST'])
def ajaxDeleteMultiple():
    quesIdArr=request.json['id']
    print(quesIdArr)
    
    for id in quesIdArr:
         sqlDbhelper.deleteQuery(id)
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
   if phrase != None:
       li=[]
       
       results = elasticSearch('http://localhost:9200/assessment/questions/_search', phrase)
       data =  results['hits']['hits']
       i = 0
       for doc in data:
          li.append([])
          li[i].append(doc['_source']['quesId'])
          li[i].append("hello")
          li[i].append(doc['_source']['question'])
          li[i].append(doc['_source']['options'])
          li[i].append(doc['_source']['correctAnswer'])
          li[i].append(doc['_source']['level'])
          li[i].append(doc['_source']['questionType'])
          li[i].append(doc['_source']['skillType'])
          li[i].append(doc['_source']['tags'])

          i=i+1
          
       return render_template("assessmentIndex.html",questions=li)
   else:
       return redirect(url_for('assessment.listQuestions'))     
   # return json.dumps({"hello":"hii"})   

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
          f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileId)) 
          parseCsvFile.delay(fileId,filename)
          #app.config['UPLOAD_FOLDER'] = 'uploadedCSV/'
          #f.save(filename)
          #f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
          #parseCsvFile.delay(fileId,filename,session['email'])
          return render_template("assessmentIndex.html",questions=results,message="File parsing is on process")
        else:
          return render_template("assessmentIndex.html",questions=results,message="File should have extension(.csv)")
      else:
        return render_template("assessmentIndex.html",questions=results,message="Choose file to upload")
   else:
      return render_template("assessmentIndex.html",questions=results)
