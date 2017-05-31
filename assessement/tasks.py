from celery import Celery
import MySQLdb
import csv 
import sys
import time
import datetime
import os
from setting import APP_STATIC
from dbHelper import Dbhelper
from flask import session
from pymongo import MongoClient

cl = Celery('tasks',backend='rpc://', broker='pyamqp://guest@localhost//')

def checkBlank(lis):
    for col in lis:
      if col!= "":
        return 0

    return 1   

def strToLi(inp,delimiter):
  li= inp.split(delimiter)
  output=""
  for value in li:
    if value.strip():
      output=output+value.strip()+","

  #return '['+','.join(li)+']'
  #inp=inp.replace(delimiter,",")
  return output[:-1]
"""
def checkCorrectAns(inp,delimiter):
   li= inp.split(delimiter)
   output=""
   for value in li:
      val=(value.strip()).upper()
      if val=='A' or val=='B' or val=='C' or val=='D' :
         output=output+val+","
      else:
         return "Not known"  

   return output[:-1]
"""
def isAnsEnter(inp,delimiter):
   li= inp.split(delimiter)
   if len(li)>1:
      return False
   else:
      linp=inp.strip().lower() 
      if linp == 'a' or linp == 'b' or linp == 'c' or linp == 'd' :
        return True

   return False      

def getLevel(level):
  return{'e':1,'m':2,'h':3}[level.strip()];

def getQuesType(quesType):
  return {'single choice':1,'multiple choice':2, 'essay':3,'short answer':4}.get(quesType,0)

def getSkillType(skillType):
  return {'logical':1,'gk':2,'reasoning':3,'theory':4,'numerical':5}.get(skillType,0)

@cl.task
def parseCsvFile(fileId,filename,email):
  
      try:
         db=MySQLdb.connect("localhost","root","root","iimjobs")
      except Exception:
        return "Can not connect to database"
      else:
        cursor=db.cursor()
        try:     
            f = open(os.path.join(APP_STATIC,fileId),'rb')
            reader = csv.reader(f)
        except IOError:
            return "file does not open"
        else: 
            for row in reader:
              break
           # li = validateCsv(reader) 
            f.seek(0)
            for row in reader:
              break

            #if len(li)==0:      
            for row in reader:
              question=row[1]
              #answer=checkCorrectAns(row[2],":")
              answer=row[2].strip()
              level=getLevel(row[3].lower())
              skillType=getSkillType(row[4].lower())
              questionType=getQuesType(row[5].lower())
              tag=strToLi(row[6],":")
              answerDescription=row[7]                  
              option='['
              for rowOpt in reader:
                if checkBlank(rowOpt):
                  if isAnsEnter(answer,":"):
                    option=option[:len(option)-1]+']'
                    cursor.execute("INSERT INTO quesBank(created_on,question,options,correct_answer,level,question_type,skill_type,tags,created_by,created_by_id,active,answer_description,flag) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                      (str(time.strftime("%Y-%m-%d %H:%M:%S")),question,option,str(answer),level,questionType,skillType,str(tag),0,0,1,answerDescription,0))
                  break    
                else:
                  option=option+'"'+rowOpt[1].strip()+'"'+','

              db.commit()    
            Dbhelper.update({"email":email},"$push",{"fileInfo":{"fileId":fileId,"filename":filename,"status":"file parsed sucessfully","date":datetime.datetime.now()}})
            #else:
             #   Dbhelper.update({"email":email},"$push",{"fileInfo":{"fileId":fileId,"filename":filename,"status":li,"date":datetime.datetime.now()}})  
              #  db.close() 
               # f.close()
      return 'success'

