import pymysql
def connectdatabase():
    return pymysql.connect(
        host= "localhost",
        user= "root",
        password='',
        port=3306,
        database='crud_products'
    )

connect=connectdatabase()

if connect:
    print("Connection to database successfully!")


