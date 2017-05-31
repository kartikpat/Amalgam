import MySQLdb

db=MySQLdb.connect("localhost","root","root","iimjobs")

cursor = db.cursor()

cursor.execute("SELECT options from quesBank;")

results = cursor.fetchall()

count=0
for row in results:
      options = row[0]
      li=options[1:len(options)-1].split(',')
      if len(li)>4:
        count=count+1

print(count)        

db.close()