import mysql.connector as mysql
from config import *

def connection(database=False):
    if database:
        return mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    return mysql.connect(
        host=host,
        user=user,
        password=password
    )

try:
    conn = connection()
except mysql.errors.ProgrammingError as e:
    print("MySQL User or password incorrect in database.ini")
    exit()
except mysql.errors.InterfaceError as e:
    print("Can't connect to MySQL Server. Make sure that the server is running")
    exit()

def createDB():
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {database}")
    cursor.close()

def createUsersTable():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name TEXT CHARSET utf8,
                    eid CHAR(8) CHARSET utf8,
                    sex CHAR(1) CHARSET utf8,
                    age INT,
                    grp CHAR(3) CHARSET utf8,
                    email VARCHAR(100) CHARSET utf8,
                    phone CHAR(10) CHARSET utf8
                )""")
    conn.commit()
    cur.close()

def createTable(table):
    cur = conn.cursor()
    cur.execute(f"""CREATE TABLE {table}(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content TEXT CHARSET utf8,
                    type CHAR(3) CHARSET utf8,
                    grp CHAR(3) CHARSET utf8,
                    triggers TEXT CHARSET utf8
                )""")
    conn.commit()
    cur.close()

cur = conn.cursor()
newDB = False
cur.execute("SHOW DATABASES")
if (database,) not in cur.fetchall():
    createDB()
    newDB = True
cur.close()
conn.close()
conn = connection(database)
if newDB:
    createUsersTable()
    createTable("admin")
    createTable("suggestions")

if __name__ == '__main__':
    print("Running this script explicitly will delete the database with name as in database.ini")
    x = input("Do you want to delete the database? [Y/n] ").upper()
    if x == 'Y' or x == 'YES':
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {database}")
        cur.close()
        print("database deleted")
    conn.close()
    print(conn)