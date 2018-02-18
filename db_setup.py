from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode



def create_database(cursor, db_name):
		try:
			cursor.execute(
					"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
			print("In create_db")
		except mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))
			exit(1)



def create_table(cursor,table):
	try:
		cursor.execute(table)
		print("Table created")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print("already exists.")
		else:
				print(err.msg)
	else:
		print("OK")

def main():
	DB_NAME = "Mesh"
	
	

	TABLE = "CREATE TABLE `Nodes1` (`ID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `Name` varchar(40) NOT NULL, `IP` varchar(40) NOT NULL, `MAC` varchar(50) NOT NULL, `LAT` float(10,6) NOT NULL, `LNG` float(10,6) NOT NULL)"

	#connect to the mysql
	cnx = mysql.connector.connect(user='root', password='toor@1234')
	cursor = cnx.cursor()


	try:
		cnx.database = DB_NAME
		print('In main try')	
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			create_database(cursor, DB_NAME)
			cnx.database = DB_NAME
			create_table(cursor, TABLE)
			print("In main ex")
		else:
			print(err)
			exit(1)
	cnx.commit()

	cursor.close()
	cnx.close()




if __name__ == "__main__":
	main()
