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

@listingQues.route('/search',methods=['POST'])
def search():
   phrase = Utility.getPostParameter('phrase')
   li=[]
   temp=[]
   results = elasticSearch('http://localhost:9200/assessment/questions/_search', phrase)
   data =  results['hits']['hits']
   for doc in data:
      temp.insert(0,doc['_source']['quesId'])
      temp.insert(1,"hello")
      temp.insert(2,doc['_source']['question'])
      temp.insert(3,doc['_source']['options'])
      temp.insert(4,doc['_source']['correctAnswer'])
      temp.insert(5,doc['_source']['level'])
      temp.insert(6,doc['_source']['questionType'])
      temp.insert(7,doc['_source']['skillType'])
      temp.insert(8,doc['_source']['tags'])
      # temp=doc['_source']['question'])
      li.append(temp)
      while len(temp) > 0 : temp.pop()
      temp=[]
   print(li)
   return render_template("assessmentIndex.html",questions=li)   
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
