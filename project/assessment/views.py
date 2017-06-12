from flask import Blueprint, Flask,request, render_template, redirect,url_for,session
from ..DBHelper.dbhelper import sqlDbhelper
import model
import json

listingQues = Blueprint('assessment',__name__,template_folder='templates')

"""@listingQues.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))
"""
@listingQues.route('/listQuestions')
def listQuestions():
    results=sqlDbhelper.getData("select * from quesBank limit 44")
    return render_template("assessmentIndex.html",questions=results)


@listingQues.route('/ajaxReceive',methods=['POST'])
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
    return redirect(url_for('assessment.listQuestions'))
    #print (quesId,ques,ans,lev,quesType,skill,tag)
    #return json.dumps({'status':'OK'})
    