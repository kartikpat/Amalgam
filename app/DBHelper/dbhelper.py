# from flask import current_app
# import mysql.connector
# from mysql.connector import errorcode



# TABLES = {}
# TABLES['employees'] = (
#     "CREATE TABLE `employees` ("
#     "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
#     "  `birth_date` date NOT NULL,"
#     "  `first_name` varchar(14) NOT NULL,"
#     "  `last_name` varchar(16) NOT NULL,"
#     "  `gender` enum('M','F') NOT NULL,"
#     "  `hire_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`)"
#     ") ENGINE=InnoDB")
# TABLES['departments'] = (
#     "CREATE TABLE `departments` ("
#     "  `dept_no` char(4) NOT NULL,"
#     "  `dept_name` varchar(40) NOT NULL,"
#     "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
#     ") ENGINE=InnoDB")
# TABLES['salaries'] = (
#     "CREATE TABLE `salaries` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `salary` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")
# TABLES['dept_emp'] = (
#     "CREATE TABLE `dept_emp` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `dept_no` char(4) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")
# TABLES['dept_manager'] = (
#     "  CREATE TABLE `dept_manager` ("
#     "  `dept_no` char(4) NOT NULL,"
#     "  `emp_no` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`),"
#     "  KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")
# TABLES['titles'] = (
#     "CREATE TABLE `titles` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `title` varchar(50) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date DEFAULT NULL,"
#     "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# class sqlDbhelper():

#     def __init__(self):
#         config = {
#             'user': current_app.config["DB_USER_NAME"],
#             'password': current_app.config["DB_USER_PASSWORD"],
#             'host': 'localhost',
#             'database': current_app.config["DATABASE_NAME"],
#             'raise_on_warnings': True
#         }
#         try:
#             self.cnx = mysql.connector.connect(**config)
#             self.cursor = self.cnx.cursor()
#         except mysql.connector.Error as err:
#           if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#           elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#           else:
#             print(err)
        

#     def create_tables(self):
#         for name, ddl in TABLES.iteritems():
#             try:
#                 print("Creating table {}: ".format(name))
#                 self.cursor.execute(ddl)
#             except mysql.connector.Error as err:
#                 if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#                     print("already exists.")
#                 else:
#                     print(err.msg)
            

#         self.cursor.close()
#         self.cnx.close()

#     # def deleteQuery(self,quesId):
#     #   self.cur.execute("DELETE FROM quesBank WHERE ques_id = %s;",(quesId))
#     #   self.sqlDb.commit()
#     #
#     # def getData(self,sqlQuery):
#     #   self.cur.execute(sqlQuery)
#     #   return self.cur.fetchall()
#     #
#     # def insertData(self,sqlQuery,data):
#     #   self.cur.execute(sqlQuery,data)
#     #   self.sqlDb.commit()
#     #   return self.cur.lastrowid
#     #
#     # def updateQuery(self,quesId, ques,correctAns,lev,quesType,skillType,tag,options):
#     #   self.cur.execute("update quesBank SET question=%s ,correct_answer=%s,level=%s,question_type=%s,skill_type=%s ,tags=%s,options=%s WHERE ques_id=%s;",(ques,correctAns,lev,quesType,skillType,tag,options,quesId))
#     #   self.sqlDb.commit()
#     #
#     # def updateLevel(self,quesId,lev):
#     #   self.cur.execute("update quesBank SET level=%s where ques_id=%s;",(lev,quesId))
#     #   self.sqlDb.commit()
#     #
#     # def updateQuestionType(self,quesId,quesType):
#     #   self.cur.execute("update quesBank SET question_type=%s where ques_id=%s;",(quesType,quesId))
#     #   self.sqlDb.commit()
#     #
#     # def updateskillType(self,quesId,skillType):
#     #   self.cur.execute("update quesBank SET skill_type=%s where ques_id=%s;",(skillType,quesId))
#     #   self.sqlDb.commit()

#     def __del__(self):
#         self.cursor.close()
#         self.cnx.close()    






#     # __listOfCollections = {
#     #
#     #         'Goldmansach': db.goldmansach,
#     #         'American Express':db.americanexp,
#     #         'Pepsico':db.pepsico,
#     #         'Taleo':db.taleo,
#     #         'Kronos': db.kronos,
#     #         'Naukri': db.naukri,
#     #         'Hike':db.hike,
#     #         'Nestle':db.nestle,
#     #         'Deloitte':db.deloitte,
#     #         'Northern Trust':db.northerntrust,
#     #         'ZS Associate':db.zs,
#     #         'Future Group':db.futuregroup,
#     #         'Landmark Group':db.landmarkgroup,
#     #         'Paytm':db.paytm,
#     #         'Societe Generale':db.SocieteG,
#     #         'Thomsan Reuters':db.thomson,
#     #         'Western Unions':db.westernunion,
#     #         'Hinduja Global':db.hindujaglobal,
#     #         'User':db.userDetail
#     #   }
