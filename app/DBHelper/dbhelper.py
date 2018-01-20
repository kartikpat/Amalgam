import MySQLdb
from flask import current_app

class sqlDbhelper():

	def __init__(self):
		self.sqlDb = MySQLdb.connect("localhost",current_app.config["DB_USER_NAME"],current_app.config["DB_USER_PASSWORD"],current_app.config["DATABASE_NAME"])
		self.cur = self.sqlDb.cursor()

	def deleteQuery(self,quesId):
		self.cur.execute("DELETE FROM quesBank WHERE ques_id = %s;",(quesId))
		self.sqlDb.commit()

	def getData(self,sqlQuery):
		self.cur.execute(sqlQuery)
		return self.cur.fetchall()

	def insertData(self,sqlQuery,data):
		self.cur.execute(sqlQuery,data)
		self.sqlDb.commit()
		return self.cur.lastrowid

	def updateQuery(self,quesId, ques,correctAns,lev,quesType,skillType,tag,options):
		self.cur.execute("update quesBank SET question=%s ,correct_answer=%s,level=%s,question_type=%s,skill_type=%s ,tags=%s,options=%s WHERE ques_id=%s;",(ques,correctAns,lev,quesType,skillType,tag,options,quesId))
		self.sqlDb.commit()

	def updateLevel(self,quesId,lev):
		self.cur.execute("update quesBank SET level=%s where ques_id=%s;",(lev,quesId))
		self.sqlDb.commit()

	def updateQuestionType(self,quesId,quesType):
		self.cur.execute("update quesBank SET question_type=%s where ques_id=%s;",(quesType,quesId))
		self.sqlDb.commit()

	def updateskillType(self,quesId,skillType):
		self.cur.execute("update quesBank SET skill_type=%s where ques_id=%s;",(skillType,quesId))
		self.sqlDb.commit()

	def __del__(self):
		self.sqlDb.close()





	# __listOfCollections = {
	#
	# 		  'Goldmansach': db.goldmansach,
	# 		  'American Express':db.americanexp,
	# 		  'Pepsico':db.pepsico,
	# 		  'Taleo':db.taleo,
	# 		  'Kronos': db.kronos,
	# 		  'Naukri': db.naukri,
	# 		  'Hike':db.hike,
	# 		  'Nestle':db.nestle,
	# 		  'Deloitte':db.deloitte,
	# 		  'Northern Trust':db.northerntrust,
	# 		  'ZS Associate':db.zs,
	# 		  'Future Group':db.futuregroup,
	# 		  'Landmark Group':db.landmarkgroup,
	# 		  'Paytm':db.paytm,
	# 		  'Societe Generale':db.SocieteG,
	# 		  'Thomsan Reuters':db.thomson,
	# 		  'Western Unions':db.westernunion,
	# 		  'Hinduja Global':db.hindujaglobal,
	# 		  'User':db.userDetail
	# 	}
