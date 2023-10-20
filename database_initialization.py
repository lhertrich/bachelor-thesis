import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

tbd = pd.read_csv(r'REDUCED_1_Table_View_Field_Definition.csv', sep=";")
kdd = pd.read_csv(r'2_Key_Definition.csv', sep=";")
idd = pd.read_csv(r'3_Interface_Definition.csv', sep=";")

try:
    connection = msql.connect(host='localhost', database='ba_bosch_data', user='root', password='root')
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS table_view_field_definition')
        cursor.execute('DROP TABLE IF EXISTS key_definition')
        cursor.execute('DROP TABLE IF EXISTS interface_definition')

        cursor.execute('CREATE TABLE table_view_field_definition(DatabaseName varchar(255), ModelCode varchar(255), EntityClassCode varchar(255), EntityStereoType varchar(255), Comment varchar(5000));')
        print("Created table")

        cursor.execute('CREATE TABLE key_definition(ModelCode varchar(255), EntityClassCode varchar(255), KeyCode varchar(255), KeyType varchar(255), IsPrimaryKey integer(2), IsAlternateKey integer(2), IsForeignKey integer(2), Stereotype varchar(255), Comment varchar(255), Description varchar(255), Annotation varchar(255), AttributeCode varchar(255), AttributeOrder integer(255));')
        print("Created table")

        cursor.execute('CREATE TABLE interface_definition(SchemaName varchar(255), SchemaID integer(255), DataCORELayer varchar(255), ObjectName varchar(255), ObjectID integer(255), ObjectType varchar(255), ObjectTypeDescription varchar(255), ObjectSQLCode_Anzahl_Character integer(255), ObjectSQLCode_First_32767_Characters text(32767));')
        print("Created table")

        for i, row in tbd.iterrows():
            sql_statement = "INSERT INTO ba_bosch_data.table_view_field_definition VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_statement, tuple(row))
            connection.commit()
        print("created first table")


        for i, row in kdd.iterrows():
            #print("row")
            sql_statement = "INSERT INTO ba_bosch_data.key_definition VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_statement, tuple(row))
            connection.commit()
        print("created second table")

        for i, row in idd.iterrows():
            sql_statement = "INSERT INTO ba_bosch_data.interface_definition VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_statement, tuple(row))
            connection.commit()
        print("created third table")

except Error as e:
    print("Error while connecting to database", e)


