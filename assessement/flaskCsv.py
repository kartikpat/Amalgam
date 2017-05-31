from flask import Flask, render_template, request,jsonify,redirect,url_for,session,send_from_directory
import os
from werkzeug import secure_filename
from tasks import parseCsvFile
from pymongo import MongoClient
import logging
from dbHelper import Dbhelper
import time

app = Flask(__name__)
app.secret_key ='sdlkfdklsjf'
app.config['UPLOAD_FOLDER'] = 'uploadedCSV/'

def allowedExtension(filename):
    return '.' in filename and filename.split('.')[1]=='csv'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if Dbhelper.findOne({"email":email,"password":password}):
            session['email']=email
            return redirect(url_for('upload'))
        else:
            return render_template("login.html",message="Enter valid credential")    

@app.route('/upload', methods = ['GET', 'POST'])  
def upload():
   user=Dbhelper.findOne({"email":session['email']})
   result=user['fileInfo']
   output=[]
   for res in result:
      output.append({"File ID":res["fileId"],"File name":res["filename"],"File status":res["status"],"Date":res['date']})
   
   if request.method == 'POST':
      f = request.files['file']
      if f:
        filename = secure_filename(f.filename)
        if allowedExtension(filename):
          fileId=filename.split('.')[0]+'_'+str(int(time.time()*1000))+'.'+filename.split('.')[1]
          f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileId)) 
          parseCsvFile.delay(fileId,filename,session['email'])
          return render_template('index.html',lis=output,message="File parsing is on process")
        else:
          return render_template('index.html',lis=output,message="Upload .csv extension file ")
      else:
        return render_template('index.html',lis=output,message="Choose file to upload")
   else:     
      return render_template('index.html',lis=output)

@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

@app.route('/download/<fileName>')
def download(fileName):
        return send_from_directory(directory='uploadedCSV/', filename=fileName,as_attachment=True)

if __name__ == '__main__':
   logging.basicConfig(filename='error.log',level=logging.DEBUG)
   app.run(debug = True)
