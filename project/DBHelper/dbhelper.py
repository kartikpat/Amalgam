from pymongo import MongoClient

client = MongoClient('localhost')
db = client.mydb

class Dbhelper():

	__listOfCollections = {

			  'Goldmansach': db.goldmansach,
			  'American Express':db.americanexp,
			  'Pepsico':db.pepsico,
			  'Taleo':db.taleo,
			  'Kronos': db.kronos,
			  'User': db.userDetail,
			  'Naukri': db.naukri

		}

	@staticmethod
	def getCollectionName(collection):
		return Dbhelper.__listOfCollections.get(collection,"")

	@staticmethod
	def getDateQuery(start,end):
		query = {'date':{
						'$gte':start,
						'$lte':end
						}}
		return query

	@staticmethod
	def findOne(collection,query):
		colection = Dbhelper.getCollectionName(collection)
		return colection.find_one(query)

	@staticmethod
	def insert(collection,query):
		colection = Dbhelper.getCollectionName(collection)
		colection.insert(query)

	@staticmethod
	def delete(collection,key,value):
	    colection = Dbhelper.getCollectionName(collection)
	    colection.remove({key : value})

	@staticmethod
	def update(collection,query,update):
		colection = Dbhelper.getCollectionName(collection)
		colection.update(query,{"$set":update})