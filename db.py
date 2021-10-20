""" File: database.py / db.py """
""" various functions to operate on MySQL database for the app """

import mysql.connector as mysql
from cfg import *


# Function to connect to MySQL server and optionally, database
def connection(database=False):
    args = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'password': PASSWORD,
        'use_pure': True
    }
    if database:
        args['database'] = database
    return mysql.connect(**args)


# Trying Connecting to MySQL server with credentials in config file
# Connection to start as soon as this script is imported
try:
    conn = connection()
except mysql.errors.ProgrammingError:
    print("MySQL User or password incorrect in config.ini")
    exit()
except mysql.errors.InterfaceError:
    print("Can't connect to the MySQL Server.")
    print("Make sure that the server is running")
    exit()


# Function to create new Database
def createDB():
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    cursor.close()

# Function to create a table of 'users' in the database
def createUsersTable():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name TEXT CHARSET utf8,
                    eid INT(6) NOT NULL,
                    sex CHAR(1) CHARSET utf8,
                    age INT,
                    grp CHAR(3) CHARSET utf8,
                    email VARCHAR(100) CHARSET utf8,
                    phone CHAR(10),
                    score_d INT,
                    score_w INT,
                    score_m INT
                )""")
    conn.commit()
    cur.close()

# Function to add a new user in the above creted table of users
def newUser(v):
    sql = """INSERT INTO users
            (name, eid, sex, age, grp, email, phone, score_d, score_w, score_m)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0, 0)"""
    values = (v['name'], v['eid'], v['sex'], v['age'],
            v['grp'], v['email'], v['phone'])
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


# Function to create table(s) for storing notification(s)
def createTable(table):
    cur = conn.cursor()
    cur.execute(f"""CREATE TABLE {table}(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content TEXT CHARSET utf8,
                    type CHAR(3) CHARSET utf8,
                    grp VARCHAR(6) CHARSET utf8,
                    triggers TEXT CHARSET utf8
                )""")
    conn.commit()
    cur.close()


# Function to store a notification content (along with type, trigger conditions etc.)
# in the database. By default, it inserts in table named 'admin'
def insert(v, table="admin"):
    sql = f"""INSERT INTO {table}
            (content, type, grp, triggers)
            VALUES (%s, %s, %s, %s)"""
    values = (v['content'], v['type'], v['grp'], v['triggers'])
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    id = cur.lastrowid
    cur.close()
    # Also, returns the row id in which this new notification is stored
    return id
    

# Function to get all stored and unsent notifications from a table.
# Can be filtered via trigger conditions optionally.
# By default, it searches in the table named 'admin'.
def pending(trig="", table="admin"):
    sql = f"""SELECT * FROM {table}
            WHERE triggers LIKE '%{trig}%'
            LIMIT 25"""
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result


# Function to get a specific stored notification
# by it's primary key i.e. id
# By default, it searches in the table named 'admin'.
def getNoti(id, table="admin"):
    sql = f"""SELECT content, type, grp
            FROM {table}
            WHERE id = %s"""
    values = (id,)
    cur = conn.cursor(buffered=True)
    cur.execute(sql, values)
    result = cur.fetchall()
    cur.close()
    return result


# Function to delete a specific stored notification
# (to mark it complete or to discard it)
# Deletes by it's primary key i.e. id
# By default, it deletes from the table named 'admin'.
def delete(id, table="admin"):
    sql = f"""DELETE FROM {table}
                WHERE id = %s"""
    values = (id,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


# Function to add score to an user fed through api
# Adds in all 3 scores i.e. daily, weekly, monthly
def addScore(eid, score):
    sql = f"""UPDATE users SET
            score_d = score_d + {score},
            score_w = score_w + {score},
            score_m = score_m + {score}
            WHERE eid = %s"""
    values = (eid,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


# Function to reset score of all users to 0
# parameters can be passed to configure whether to reset weekly or monthly scores or not.
def resetScore(week=False, month=False):
    if week:
        x = 'w'
    elif month:
        x = 'm'
    else:
        x = 'd'
    sql = f"""UPDATE users
            SET score_{x} = 0"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


# Function to change trigger conditions of a specific notification
# by it's primary key i.e. id
# By default, it updates the notification in the table named 'admin'.
def changeTrigger(id, trig, table="admin"):
    sql = f"""UPDATE {table}
            SET triggers = '{trig}'
            WHERE id = %s"""
    values = (id,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


# Function to return list of all users stored in the database
# Returns group, email, phone, employee_id and scores of users
# Alternatively, can search for only one user by passing their employee_id
def getUsers(eid=False):
    if eid:
        sql = f"""SELECT grp, email, phone, score_d, score_w, score_m
                FROM users WHERE eid = {eid}"""
    else:
        sql = "SELECT grp, email, phone, score_d, score_w, score_m, eid FROM users"
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result


# This section to run as soon as this script is imported
# To check if the database for this notificatoin engine exists or not
# The name of database is taken from the config file
# If not existing already (e.g. running this engine for the first time),
# automatically creates the database and 3 tables - users, admin, suggestions
# Also connects to the database of MySQL server
cur = conn.cursor(buffered=True)
newDB = False
cur.execute("SHOW DATABASES")
if (DATABASE,) not in cur.fetchall():
    createDB()
    newDB = True
cur.close()
conn.close()
conn = connection(DATABASE)
if newDB:
    createUsersTable()
    createTable("admin")
    createTable("suggestions")


# Running this script explicitly to delete the database
# Implemented for developement purposes only
# No need to run this script explicitly in production
if __name__ == '__main__':
    # Getting confirmation from the user
    print("Running this script explicitly will delete the database with name as in config.ini")
    x = input("Do you want to delete the database? [Y/n] ").upper()
    if x == 'Y' or x == 'YES':
        # Deleting the database with name as in config file
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
        cur.close()
        print("database deleted")
    print(conn)
    conn.close()
    