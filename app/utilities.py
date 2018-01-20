from flask import request,session
# import datetime
# from .DBHelper.dbhelper import Dbhelper
#
# # def getUrlParameter(param):
# #     return request.args.get(param)
# #
# # def getUrlParameterList(param):
# #     return request.args.getlist(param)
#
# def ISODateToString(date):
#     da = datetime.datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S")
#     return str(da.day) + "-" + da.strftime("%b") + "-" + str(da.year)
#
# def StringToISODate(date):
#     string = datetime.datetime.strptime(date, "%d-%m-%Y")
#     ISODate = datetime.datetime(string.year,string.month,string.day,0,0,0,0)
#     return ISODate
#
# def getList(colectn, query):
#     collection = Dbhelper.getCollectionName(colectn)
#     result = collection.find(query).sort([("date",-1)])
#     return result
#
# # def getPostParameter(param):
# #     result = request.form
# #     return result.get(param,None)

def isLoggedIn():
    boolean = 0
    if 'email' in session:
        boolean = 1
    return boolean
