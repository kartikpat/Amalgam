from pymongo import MongoClient
import MySQLdb

client = MongoClient('localhost')
db = client.mydb

sqlDb = MySQLdb.connect("localhost","root","root","iimjobs")
cur = sqlDb.cursor()

class sqlDbhelper():

	

	@staticmethod
	def deleteQuery(quesId):
		cur.execute("DELETE FROM quesBank WHERE ques_id = %s;",(quesId))
		sqlDb.commit()

	@staticmethod
	def getData(sqlQuery):
		cur.execute(sqlQuery)
		return cur.fetchall()

	@staticmethod
	def updateQuery(quesId, ques,correctAns,lev,quesType,skillType,tag,options):
		cur.execute("update quesBank SET question=%s ,correct_answer=%s,level=%s,question_type=%s,skill_type=%s ,tags=%s,options=%s WHERE ques_id=%s;",(ques,correctAns,lev,quesType,skillType,tag,options,quesId))
		sqlDb.commit()

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

	@staticmethod
	def arrUpdate(collection,query,update,updateModifier):
		colection = Dbhelper.getCollectionName(collection)
		colection.update(query,{updateModifier:update})
