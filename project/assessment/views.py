from flask import Blueprint, Flask,request, render_template, redirect,url_for,session
from ..DBHelper.dbhelper import sqlDbhelper
import model

listingQues = Blueprint('assessment',__name__,template_folder='templates')

"""@listingQues.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))
"""
@listingQues.route('/listQuestions')
def listQuestions():
	results=sqlDbhelper.getData("select * from quesBank limit 50")
	return render_template("assessmentIndex.html",questions=results)

	
