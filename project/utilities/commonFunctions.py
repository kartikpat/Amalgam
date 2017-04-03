from flask import request,session
import datetime
from ..DBHelper.dbhelper import Dbhelper

class Utility:

	@staticmethod
	def getUrlParameter(param):
		return request.args.get(param)

	@staticmethod
	def getUrlParameterList(param):
		return request.args.getlist(param)

	@staticmethod
	def ISODateToString(date):
		da = datetime.datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S")
		return str(da.day) + "-" + da.strftime("%b") + "-" + str(da.year)
	
	@staticmethod
	def StringToISODate(date):
		string = datetime.datetime.strptime(date, "%Y-%m-%d")
		ISODate = datetime.datetime(string.year,string.month,string.day,0,0,0,0)
		return ISODate

	@staticmethod
	def getList(colectn, query,lim=0):
		collection = Dbhelper.getCollectionName(colectn)
		result = collection.find(query).limit(lim)
		return result

	@staticmethod
	def getPostParameter(param):
		result = request.form   		
		return result[param]

	@staticmethod
	def isLoggedIn():
		boolean = 0
		if 'email' in session:
			boolean = 1
		return boolean    


	