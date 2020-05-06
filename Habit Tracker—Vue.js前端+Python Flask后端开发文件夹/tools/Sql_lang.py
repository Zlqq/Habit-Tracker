# -*- coding: utf-8 -*-
#数据库
import sqlite3   
#连接Vue.db数据库
def conn_mysql():
    try: 
        DB_FILES = 'db/Vue.db'
        conn = sqlite3.connect(DB_FILES)  #1
        cur = conn.cursor() #2
        print ("Opened database successfully.")
    except Exception as e:
        print( "Error in open operation.",e)   
    finally:
        return conn, cur
#查询数据库
def find_mysql(sql):
    conn,cur = conn_mysql()
    result = []
    try:
        cur.execute(sql)
        rows = cur.fetchall() 
        for i in rows:
            result.append(i)
        print("数据查询成功")
    except:
        print("数据查询失败")
    finally:
        conn.close()
        return result
        
#插入数据
def insert_mysql(sql):
    conn,cur = conn_mysql()
    try:
        cur.execute(sql)
        conn.commit()
        res = True
        msg = "Record successfully added."
    except: 
        conn.rollback()
        res = False
        msg = "error in insert operation."
    finally:
        conn.close()
        return msg,res
        
#更新数据库
def update_mysql(sql):
    conn,cur = conn_mysql()
    try:
        conn.execute(sql)
        conn.commit() 
        #print ("Total number of rows updated:", conn.total_changes)
        msg = "Record successfully updated."
        res = True
    except:
        conn.rollback() 
        res = False
        msg = "error in update operation."
    finally:
        conn.close()
        return msg,res
    
#删除数据
def remove_mysql(sql):
    conn,cur = conn_mysql()
    try:
        cur.execute(sql)
        conn.commit()
        msg = "Record successfully removed."
    except:
        msg = 'erroe in delete operation.'
        conn.rollback()
    finally:
        conn.close()
        return msg

#获取table中的全部usernames/xms
def find_items(item,table):
    conn,cur = conn_mysql()
    result = []
    try:
        sql = "select {} from {}".format(item,table)
        cur.execute(sql)
        result = cur.fetchall() 
        print("{}查询成功".format(item))
    except:
        print("{}查询失败".format(item))
    finally:
        conn.close()
        return result
def isAdmin(name,pswd):
    conn,cur = conn_mysql()
    result = []
    try:
        sql = "select * from admin where Name = '{}' and Password = '{}'".format(name,pswd)
        cur.execute(sql)
        result = cur.fetchall()
        print("{}查询成功".format(name))
    except:
        print("{}查询失败".format(name)) 
    finally:
        conn.close()
    return True if len(result) > 0 else False 

#获取table当前用户名的密码or验证码
def find_item(item,table,nm):
    conn,cur = conn_mysql()
    result = []
    try:
        sql = "select {} from {} where USERNAME = '{}'".format(item,table,nm)
        cur.execute(sql)
        rows = cur.fetchall()
        for i in rows:
            result.append(i[0])
        print("{}查询成功".format(item))
    except:
        print("{}查询失败".format(item))
    finally:
        conn.close()
        return result
      
#验证该用户名是否重复注册
def Isregister(nm):
    #定义register表格里的usernames
    rows = find_items("USERNAME","register")   
    names = []
    for i in rows:
        names.append(i[0])
    names_list = set(names)    
    return True if nm in names_list else False

#验证该昵称是否已经被注册
def IsXmUsed(xm):
    #定义register表格里的usernames
    rows = find_items("XM","register")  
    xms = []
    for i in rows:
        xms.append(i[0])
    xms_list = set(xms)
    return True if xm in xms_list else False 

#验证是否已经得到验证码
def Isgetsms(nm):
    #获取table表格里的usernames      
    rows = find_items("USERNAME","getsms")  
    names = []
    for i in rows:
        names.append(i[0])
    names_list = set(names) 
    return True if nm in names_list else False
 
#验证密码/验证码是否与数据库中的匹配
def Ismatch(item,table,nm, variable):
    item_list = set(find_item(item,table,nm))  
    return True if variable in item_list else False 
#获取inputDetail里的记录（Standard,Date）/通过username和title
def find_records(item1,item2,table,xm,title):
    conn,cur = conn_mysql()
    result=[]
    standard=[]
    date=[]
    try:
        sql = "select {},{} from {} where USERNAME = '{}' and TITLE ='{}'".format(item1,item2,table,xm,title)
        cur.execute(sql)
        rows = cur.fetchall()
        
        for i in rows:
            standard.append(i[0])
            date.append(i[1])
        
        print("{}查询成功".format(item1))
        result.append(standard)
        result.append(date)
        print(result)
    except:
        print("{}查询失败".format(item1))
    finally:
        conn.close()
        return result
#获取inoutDetail的日期
def find_dates(username,title,datetime):
    conn,cur = conn_mysql()
    result = []
    try:
        sql = "select * from inputDetail where username = '{}' and title = '{}' and date = '{}'".format(username,title,datetime)
        cur.execute(sql)
        result = cur.fetchall() 
        print("{}查询成功".format(item))
    except:
        print("{}查询失败".format(item))
    finally:
        conn.close()
        return result
      
#验证该日期是否重复记录
def Isdate(username,title,datetime):
    dates_list = set(find_dates(username,title,datetime))
    return True if len(dates_list) else False

#根据用户名和习惯查找记录
def find_habit(username,title):
    conn,cur = conn_mysql()
    results = []
    try:
        sql = "select * from habit where username = '{}' and title = '{}'".format(username,title)
        cur.execute(sql)
        results = cur.fetchall() 
        print("数据查询成功".format(item))
    except:
        print("数据查询失败".format(item))
    finally:
        conn.close()
        return results

#验证用户是否重复添加记录
def Ishabit(username,title):
    habit_list = set(find_habit(username,title)) 
    return True if len(habit_list) else False
