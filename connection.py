import pymysql

def connectdatabase():
    return pymysql.connect(
        host= "localhost",
        user= "root",
        password='',
        port=3306,
        database='inventory_flask_db'
    )

connection=connectdatabase()

if connection:
    print("Connection to database successfully!")


