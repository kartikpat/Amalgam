from celery import Celery
# import boto.ses
import boto3
import MySQLdb
import time
import csv
import os
from pymongo import MongoClient
import datetime
from DBHelper.dbhelper import Dbhelper,sqlDbhelper



cl = Celery('tasks',backend='rpc://', broker='pyamqp://guest@localhost//')
CELERY_IMPORTS=("tasks")

def getMailConnection():
    AWS_ACCESS_KEY = 'AKIAIBKUBCW3L26UNWDA'  
    AWS_SECRET_KEY = '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'

    mailConnection = boto3.client('ses',
                'us-west-2',
                aws_access_key_id=AWS_ACCESS_KEY, 
                aws_secret_access_key=AWS_SECRET_KEY
            )
    return mailConnection

mailConnection=getMailConnection()

def validateCSV(reader):
    li=[]
    i=1
    for row in reader:
        break

    for row in reader:
      i=i+1
      # question=row[1]
      #answer=checkCorrectAns(row[2],":")
      answer=row[2].strip()
      level=getLevel(row[3].lower())
      skillType=getSkillType(row[4].lower())
      questionType=getQuesType(row[5].lower())
      # tag=strToLi(row[6],":")          
      if level==None or skillType==None or questionType==None or not isAnsEnter(answer,":"):
        li.append(i)
      
      for rowOpt in reader:
        i=i+1
        if checkBlank(rowOpt):
             break    

    return li    

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

  return output[:-1]

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
  return{'e':1,'m':2,'h':3}.get(level.strip(),None);

def getQuesType(quesType):
  return {'single choice':1,'multiple choice':2, 'essay':3,'short answer':4}.get(quesType,None)

def getSkillType(skillType):
  return {'logical':1,'gk':2,'reasoning':3,'theory':4,'numerical':5}.get(skillType,None)


@cl.task(name="project.tasks.sendMail")
def sendMail(to,subject,body):
    from_addr='crawler@iimjobs.com'
    # return mailConnection.send_email(from_addr,subject,None,to,format='text',text_body=body,html_body =None)
    return mailConnection.send_email(Source=from_addr,Destination={"ToAddresses":[to]},Message={'Subject':{'Data':subject,'Charset': 'UTF-8'},'Body':{'Text':{'Data':body,'Charset': 'UTF-8'},'Html': {'Data': body ,'Charset': 'UTF-8'}}})

# Source='Cron Server-2<info@iimjobs.com>',
# Destination={'ToAddresses': ['"Roshan"<roshan@iimjobs.com>','"Amit"<amit.verma@iimjobs.com>','"Yugal"<yugal@iimjobs.com>','"Jaspal Singh"<jaspal.singh@iimjobs.com>','"Triptee"<triptee@iimjobs.com>'],},
# Message={'Subject': {'Data': 'JobFeed not running please check '+str(num),'Charset': 'UTF-8'},'Body': {'Text': {'Data': 'Cron jobfeed not working for list' ,'Charset': 'UTF-8'},'Html': {'Data': 'Cron jobfeed not working for list' ,'Charset': 'UTF-8'}}},
# ReplyToAddresses=['info@iimjobs.com'],
# ReturnPath='info@iimjobs.com'

# {'Subject': {'Data': 'JobFeed not running please check '+str(num),'Charset': 'UTF-8'},'Body': {'Text': {'Data': 'Cron jobfeed not working for list' ,'Charset': 'UTF-8'},'Html': {'Data': 'Cron jobfeed not working for list' ,'Charset': 'UTF-8'}}}


@cl.task(name="project.tasks.parseCsvFile")
def parseCsvFile(fileId,filename,email):
  
        dbObj=sqlDbhelper()
        try:    
            f = open(os.path.join('assessment/uploadedCSV/',fileId),'rb')
            reader = csv.reader(f)
        except IOError:
          return "file does not open"
        else:
           #  for row in reader:
           #    break
            li = validateCSV(reader) 
            # print(li)
            f.seek(0)
            for row in reader:
              break

            if len(li)==0:      
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
                      dbObj.insertData("INSERT INTO quesBank(created_on,question,options,correct_answer,level,question_type,skill_type,tags,created_by,created_by_id,active,answer_description,flag) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (str(time.strftime("%Y-%m-%d %H:%M:%S")),question,option,str(answer),level,questionType,skillType,str(tag),0,0,1,answerDescription,0))
                    break    
                  else:
                    option=option+'"'+rowOpt[1].strip()+'"'+','

              # db.commit()
              # db.close()

              # mongoDb.userDetail.update({'email':email},{"$push":{"permission.Assessment.uploadedCSV":{"fileName":filename,"fileId":fileId,"date":datetime.datetime.now(),"status":"No error in file"}}})
              Dbhelper.arrUpdate('User',{'email':email},{"permission.Assessment.uploadedCSV":{"fileName":filename,"fileId":fileId,"date":datetime.datetime.now(),"status":"success"}},"$push")
              return 'success'    
            else:
               # db.close()
               Dbhelper.arrUpdate('User',{'email':email},{"permission.Assessment.uploadedCSV":{"fileName":filename,"fileId":fileId,"date":datetime.datetime.now(),"status":li}},"$push")

               # mongoDb.userDetail.update({'email':email},{"$push":{"permission.Assessment.uploadedCSV":{"fileName":filename,"fileId":fileId,"date":datetime.datetime.now(),"status":li}}})
               f.close()
               return "error in file" 


            