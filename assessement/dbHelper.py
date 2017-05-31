from pymongo import MongoClient

client = MongoClient('localhost')
db = client.fileStatus
collection=db.csvFileStatus

class Dbhelper():

	@staticmethod
	def findOne(query):
		return collection.find_one(query)

	@staticmethod
	def insert(query):
		collection.insert(query)

	@staticmethod
	def delete(key,value):
	    collection.remove({key : value})

	@staticmethod
	def update(query,operator,update):
		collection.update(query,{operator:update})
