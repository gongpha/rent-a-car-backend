""" Database utilities """
from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()

def init_db(app : Flask) :
    """ Initialize the database """
    mysql.init_app(app)

# อย่าใช้
# execute_sql("SELECT * from customers WHERE first_name = " + first_name)
# แต่ใช้แบบนี้แทน
# execute_sql("SELECT * from customers WHERE first_name = %s", first_name)
# เอาไว้กัน SQL Injection

def execute_sql(sql : str, *args) :
    """ Run SQL query and return the multiple results """
    # รัน SQL ; ใช้กับ SELECT ที่จะได้ผลลัพธ์กลับมาหลาย ๆ แถว
    # อย่างพวกข้อมูลที่มาหลายอันเช่น สาขาทุกสาขา รถทุกคัน ลูกค้าทุกคน และอื่น ๆ
    cursor = mysql.get_db().cursor()
    cursor.execute(sql, args)
    output = cursor.fetchall()
    return output # return เป็น list ของ tuple หรือ list ว่างถ้าไม่เจอ

def execute_sql_one(sql : str, *args) :
    """ Run SQL query and return the one result """
    # รัน SQL ; ใช้กับ SELECT ที่จะได้ผลลัพธ์กลับมาเพียงแค่ 1 แถว
    # อย่างพวกข้อมูลเดี่ยว ๆ เช่นข้อมูลลูกค้าตาม ID ข้อมูลรถตาม ID และอื่น ๆ
    cursor = mysql.get_db().cursor()
    cursor.execute(sql, args)
    output = cursor.fetchone()
    return output # return เป็น tuple หรือ None ถ้าไม่เจอ

def commit_sql(sql : str, *args) :
    cursor = mysql.get_db().cursor()
    cursor.execute(sql, args)
    mysql.get_db().commit()

def commit_sqls(sqls : list[str], argss : list[tuple]) :
    cursor = mysql.get_db().cursor()
    for s, a in zip(sqls, argss) :
        if s == "" : continue
        cursor.execute(s, a)
    mysql.get_db().commit()