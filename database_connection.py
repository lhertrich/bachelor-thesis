import mysql.connector as msql
from mysql.connector import Error

class DatabaseConnection:

    def __init__(self):
        try: 
            connection = msql.connect(host='localhost', database='ba_bosch_data', user='root', password='root')
            self.connection = connection
            if connection.is_connected:
                self.cursor = connection.cursor()
        except Error as e:
            print("Error while connecting to database",e)

    def execute_query(self, query):
        try: 
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print("Error while executing query",e)

