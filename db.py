import mysql.connector as mysql
from cfg import *

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


try:
    conn = connection()
except mysql.errors.ProgrammingError:
    print("MySQL User or password incorrect in config.ini")
    exit()
except mysql.errors.InterfaceError:
    print("Can't connect to the MySQL Server.")
    print("Make sure that the server is running")
    exit()


def createDB():
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    cursor.close()

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
    return id
    

def pending(trig="", table="admin"):
    sql = f"""SELECT * FROM {table}
            WHERE triggers LIKE '%{trig}%'
            LIMIT 25"""
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

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

def delete(id, table="admin"):
    sql = f"""DELETE FROM {table}
                WHERE id = %s"""
    values = (id,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()

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

def changeTrigger(id, trig):
    sql = f"""UPDATE admin
            SET triggers = '{trig}'
            WHERE id = %s"""
    values = (id,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()

def getUsers(eid=False):
    if eid:
        sql = f"""SELECT grp, email, phone, score_d, score_w, score_m
                FROM users WHERE eid = {eid}"""
    else:
        sql = "SELECT grp, email, phone, score_d, score_w, score_m FROM users"
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

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

if __name__ == '__main__':
    print("Running this script explicitly will delete the database with name as in config.ini")
    x = input("Do you want to delete the database? [Y/n] ").upper()
    if x == 'Y' or x == 'YES':
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
        cur.close()
        print("database deleted")
    print(conn)
    conn.close()
    