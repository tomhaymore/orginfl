import MySQLdb
#http://scienceoss.com/mysqldb-accessing-mysql-databases-from-python/
#http://code.google.com/edu/tools101/mysql.html#Setting_Up_the_Tables
#http://dev.mysql.com/doc/refman/5.1/en/entering-queries.html

class DataBase:
	"""
	Simple Wrapper for a Database Class, connection is established once and the cursor is set in the init method.
	Simplifies such that we don't have to use self.dbcursor.execute("command") anymore. 
	Merely need to pass in commands, fields, and conditions as strings after initializing.
	"""
	def __init__(self, host='127.0.0.1', user='root', passwd='', db='defaultDatabase'):
		conn = MySQLdb.connect(host, user, passwd, db) #Connect to database
		self.db = conn #Connected database set
		self.dbcursor = self.db.cursor() #Cursor initialized

	def createDatabase(self, dbName):
		self.dbcursor.execute("CREATE DATABASE %(database)s;" % {"database" : dbName})
		self.dbcursor.execute("USE %(database)s;" % {"database" : dbName})

	def dropDatabase(self, dbName):
		self.dbcursor.execute("DROP DATABASE %(database)s;" % {"database" : dbName})
		
	def createTable(self, name, fields):
		self.dbcursor.execute("CREATE TABLE %(name)s (%(fields)s);" % {"name": name, "fields": fields})

	def dropTable(self, name): #No Error handling for table does not exist
		self.dbcursor.execute("DROP TABLE %(name)s;" % {"name": name})
				
	def insert(self, tableName, fields = "", generalDataStruct = None):
		if isinstance(generalDataStruct, dict): #Dict of fields and associated values
			for k, v in generalDataStruct.items():
				if isinstance(v, int):
					fields += k + "=" + v + ", "
				else:
					if v.find("\"") >= 0:
						v = v.replace("\"", "")
					if v.find("\\") >= 0:
						v = v.replace("\\", "")
					fields += k +"=\"" + v + "\", "
			fields = fields[:fields.__len__()-2]
		elif isinstance(generalDataStruct, list): #List of already defined fields
			for item in generalDataStruct:
				fields += item + "\", "
			fields = fields[:fields.__len__()-2]
		self.dbcursor.execute("insert into %(tableName)s set %(fields)s;" % {"tableName" : tableName, "fields" : fields});
					
	def update(self, tableName, fields, conditionsDataStruct): #Rewrite eventually
		self.dbcursor.execute("update %(tableName)s set %(fields)s" % {"tableName" : tableName, "fields" : fields} + where(conditionsDataStruct));

	def delete(self, tableName, conditionsDataStruct): #Rewrite eventually
		self.dbcursor.execute("delete from %(tableName)s" % {"tableName" : tableName} + where(conditionsDataStruct));

	def where(self, table, fields = "", conditionsDataStruct = None):
		conditions = ""
		if isinstance(conditionsDataStruct, dict): #Dict of associated conditions
			for k, v in conditionsDataStruct.items():
				if isinstance(v, int):
					fields += k + "=" + v + "AND" 
				if v.find("\"") >= 0:
					v = v.replace("\"", "")
				conditions += k +"=\"" + v + "\", "
			conditions = conditions[:conditions.__len__()-2]
			return "WHERE " + conditions
		else: #Flat String
			return "WHERE " + conditionsDataStruct
				
	#__________________Debugging Printing Methods Mostly_____________________#	
	def getTableNames(self): #Returns list of table names
		self.dbcursor.execute("show tables;") #Execute cursor to show tables
		tableNames =[]
		for row in self.dbcursor.fetchall(): #Fetch all names for database
			tableNames.append(row[0])
			print row[0] #Print each table name
		return tableNames

	def getDBNames(self): #Returns list of database names
		self.dbcursor.execute("show databases;") #Execute cursor to show tables
		dbNames =[]
		for row in self.dbcursor.fetchall(): #Fetch all names for database
			dbNames.append(row[0])
			print row[0] #Print each table name
		return dbNames
	#________________________________________________________________________#

if __name__ == "__main__":
	print "This file is not an executable and merely defines the DataBase and Table classes"

"""	def select(self, tableName, fields ="*", conditions="", printInfo=False): #Rewrite eventually
		if printInfo is True:
			self.dbcursor.execute("describe %(name)s;" % {"name": tableName})
			listOfKeys = []
			for row in self.dbcursor.fetchall():
				listOfKeys.append(row[0])
			print listOfKeys
			print ""
		self.dbcursor.execute("select %(fields)s from %(tableName)s %(conditions)s;" % {"fields" : fields, "tableName" : tableName, "conditions" : conditions});
		for row in self.dbcursor.fetchall():
				print row"""
	