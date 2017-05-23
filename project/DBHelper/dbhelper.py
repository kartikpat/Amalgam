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
			  'Naukri': db.naukri,
			  'Hike':db.hike,
			  'Nestle':db.nestle,
			  'Deloitte':db.deloitte,
			  'Northern Trust':db.northerntrust,
			  'ZS Associate':db.zs,
			  'Future Group':db.futuregroup,
			  'Landmark Group':db.landmarkgroup,
			  'Paytm':db.paytm,
			  'Societe Generale':db.SocieteG,
			  'Thomsan Reuters':db.thomson,
			  'Western Unions':db.westernunion,
			  'Hinduja Global':db.hindujaglobal,
			  'User':db.userDetail
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
