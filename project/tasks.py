from celery import Celery
import boto.ses

cl = Celery('tasks',backend='rpc://', broker='pyamqp://guest@localhost//')
CELERY_IMPORTS=("tasks")

def getMailConnection():
    AWS_ACCESS_KEY = 'AKIAIBKUBCW3L26UNWDA'  
    AWS_SECRET_KEY = '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'

    mailConnection = boto.ses.connect_to_region(
                'us-west-2',
                aws_access_key_id=AWS_ACCESS_KEY, 
                aws_secret_access_key=AWS_SECRET_KEY
            )
    return mailConnection

mailConnection=getMailConnection()

@cl.task(name="project.tasks.sendMail")
def sendMail(to,subject,body):
    from_addr='crawler@iimjobs.com'
    return mailConnection.send_email(from_addr,subject,None,to,format='text',text_body=body,html_body =None)