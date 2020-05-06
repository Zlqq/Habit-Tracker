# -*- coding: UTF-8 -*-
#import altair as alt
#alt.data_transformers.enable('default', max_rows=None)
#import pandas as pd
#import json
#import random
from flask import Flask,request,render_template,url_for,redirect,jsonify
from flask_cors import CORS  #跨域

#引入文件(zlq)
import tools.Validate as validate  
import tools.Send_email as email
import tools.Sql_lang as statement

#flask
app = Flask(__name__)
app.config.from_object(__name__)

#跨域(zlq)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



#############################################################################################################(Cassie_flask_start)
#404   
@app.errorhandler(404)
def page_not_found(e):
    return  render_template("404.html"), 404
#500
@app.errorhandler(500)
def internal_server_error(e):
    return  render_template("500.html"), 500
       
#呈现完整数据库
adminname=''
adminpswd=''
@app.route('/',methods = ['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        nm = request.form['nm']
        mm = request.form['mm']
        if statement.isAdmin(nm,mm):
            global adminname, adminpswd
            adminname = nm
            adminpswd = mm
            print(adminname)
            return redirect(url_for('find_all'))
    else:
        return render_template('adminlogin.html')
    return render_template('adminlogin.html')
@app.route('/admin')
def find_all():
    print(adminname)
    if adminname == '' or adminpswd == '':
        return render_template('adminlogin.html')
    else:
        sql1 = "select * from register"
        rows1 = statement.find_mysql(sql1)
        sql2 = "select * from habit"
        rows2 = statement.find_mysql(sql2)
        sql3 = "select * from inputDetail"
        rows3 = statement.find_mysql(sql3)
        sql4 = "select * from admin"
        rows4 = statement.find_mysql(sql4)
        sql5 = "select * from addAdvice"
        rows5 = statement.find_mysql(sql5)
        return render_template("database.html", rows1 = rows1, rows2 = rows2, rows3 = rows3, rows4 = rows4, rows5 = rows5)
    
#删除该条记录
@app.route('/del')
def remove_record():
    n = request.args['id']
    sql = "DELETE FROM register WHERE ID = {}".format(n)
    msg = statement.remove_mysql(sql)
    print(msg)
    return redirect(url_for('find_all')) #url_for带的是def函数名
@app.route('/del2')
def remove_record2():
    n = request.args['id']
    sql = "DELETE FROM habit WHERE ID = {}".format(n)
    msg = statement.remove_mysql(sql)
    print(msg)
    return redirect(url_for('find_all'))
@app.route('/del3')
def remove_record3():
    n = request.args['id']
    sql = "DELETE FROM inputDetail WHERE ID = {}".format(n)
    msg = statement.remove_mysql(sql)
    print(msg)
    return redirect(url_for('find_all'))
@app.route('/del4')
def remove_record4():
    n = request.args['id']
    sql = "DELETE FROM admin WHERE ID = {}".format(n)
    msg = statement.remove_mysql(sql)
    print(msg)
    return redirect(url_for('find_all'))
@app.route('/del5')
def remove_record5():
    n = request.args['id']
    sql = "DELETE FROM addAdvice WHERE ID = {}".format(n)
    msg = statement.remove_mysql(sql)
    print(msg)
    return redirect(url_for('find_all'))

#切换到更新记录页面
@app.route('/update')
def update_record():
    n = request.args['id'] 
    sql = "select * from register where ID = {}".format(n)
    rows = statement.find_mysql(sql)
    return render_template("edit.html", rows = rows)
@app.route('/update2')
def update_record2():
    n = request.args['id'] 
    sql = "select * from habit where ID = {}".format(n)
    rows = statement.find_mysql(sql)
    return render_template("edit2.html", rows = rows)
@app.route('/update3')
def update_record3():
    n = request.args['id'] 
    sql = "select * from inputDetail where ID = {}".format(n)
    rows = statement.find_mysql(sql)
    return render_template("edit3.html", rows = rows)
@app.route('/update4')
def update_record4():
    n = request.args['id'] 
    sql = "select * from admin where ID = {}".format(n)
    rows = statement.find_mysql(sql)
    return render_template("edit4.html", rows = rows)
#保存记录
@app.route('/save',methods = ['POST', 'GET'])
def save_record(): 
    if request.method == 'POST':
        n = request.form['number']
        username = request.form['nm']
        xm = request.form['xm']
        password = request.form['ps']
        code = request.form['cd']
        sql = "UPDATE register SET USERNAME = \'%s\', XM = \'%s\', PASSWORD = \'%s\', CODE = \'%s\' WHERE ID = \'%s\' "%(username,xm,password,code,n)
        msg,res = statement.update_mysql(sql)
        print(msg)
        return redirect(url_for('find_all'))
    else:
        return redirect(url_for('update_record'))
@app.route('/saveA',methods = ['POST', 'GET'])
def save_recordA(): 
    if request.method == 'POST':
        n = request.form['number']
        username = request.form['nm']
        xg = request.form['xg']
        mb = request.form['mb']
        sz = int(request.form['sz'])
        rq = int(request.form['rq'])
        sql = "UPDATE habit SET USERNAME = \'%s\', TITLE = \'%s\', HABIT_OBJECT = \'%s\', OBJECT_NUMBER = \'%s\', DATETIME = \'%s\' WHERE ID = \'%s\' "%(username,xg,mb,sz,rq,n)
        msg,res = statement.update_mysql(sql)
        print(msg)
        return redirect(url_for('find_all'))
    else:
        return redirect(url_for('update_record'))
@app.route('/saveB',methods = ['POST', 'GET'])
def save_recordB(): 
    if request.method == 'POST':
        n = request.form['number']
        username = request.form['nm']
        xg = request.form['xg']
        mb = request.form['mb']
        sz = int(request.form['sz'])
        rq = request.form['rq']
        wc = request.form['wc']
        sql = "UPDATE inputDetail SET USERNAME = \'%s\', TITLE = \'%s\', ATTR = \'%s\', STANDARD = \'%s\', DATE = \'%s\', Finished = \'%s\' WHERE ID = \'%s\' "%(username,xg,mb,sz,rq,wc,n)
        msg,res = statement.update_mysql(sql)
        print(msg)
        return redirect(url_for('find_all'))
    else:
        return redirect(url_for('update_record'))
@app.route('/saveC',methods = ['POST', 'GET'])
def save_recordC(): 
    if request.method == 'POST':
        n = request.form['number']
        username = request.form['nm']
        mm = request.form['mm']
        
        sql = "UPDATE admin SET Name = \'%s\', Password = \'%s\' WHERE ID = \'%s\' "%(username,mm,n)
        msg,res = statement.update_mysql(sql)
        print(msg)
        return redirect(url_for('find_all'))
    else:
        return redirect(url_for('update_record'))
###############################################################################################################(Cassie api_start)     
#验证码api
@app.route('/api/GetSms/', methods = ['POST', 'GET'])
def GetSms():
     T = '验证码已成功发送！'
     F = '获取验证码失败！'
     response_object = {'status': 'success'}
     if request.method == 'POST':
         data = request.get_json()
         username = data['username']
         #验证邮箱是否合法
         vEmail = validate.ValidateEmail(username)
         #如果该邮箱合法
         if vEmail == True:
            #验证该邮箱是否已注册
            #未注册账号获取验证码:注册___________________ 获取getsms table的验证码
            if statement.Isregister(username) != True:
                insert_v = False 
                update_v = False
                #随机获取验证码
                new_code = ''
                new_code = email.get_code()
                #如果生成新密码、更新数据库、发送邮件成功
                if validate.ValidateCode(new_code) == True: 
                    #如果该邮箱从未获取过验证码：插入insert数据库
                    if statement.Isgetsms(username) != True:
                        #getsms插入记录
                        sql = "insert into getsms values (null,\'%s\',\'%s\')"%(username,new_code)
                        msg, insert_v  = statement.insert_mysql(sql)
                    #如果该邮箱曾获取过验证码：更新update数据库
                    else:
                        #getsms更新记录
                        sql = "UPDATE getsms SET CODE = \'%s\' WHERE USERNAME = \'%s\' "%(new_code,username)
                        msg, update_v = statement.update_mysql(sql) 
                    #如果插入or更新成功
                    if update_v == True or insert_v  == True:
                        #发送验证码
                        sed = email.send_mail(username, new_code)
                        if sed == True:
                            response_object['message'] = T
                            response_object['resCode'] = 101
                        else:
                            response_object['message'] = '无效邮箱，请重新尝试！'
                    else:
                         response_object['message'] = F
                #如果生成新密码、更新数据库、发送邮件失败
                else:
                    response_object['message'] = F
            #已注册账号获取验证码：登录______________获取register table的验证码
            else:   
                 origional_code = statement.find_item('CODE','register',username)[0]  #获取register表格里该用户名的验证码
                 print("以前：{}".format(origional_code))
                 #获取新密码
                 code = ''
                 code = email.get_code()
                 print("现在：{}".format(code))
                 #如果生成新密码、更新数据库、发送邮件成功
                 if validate.ValidateCode(code) == True: 
                     #更新数据库
                     sql = "UPDATE register SET CODE = \'%s\' WHERE USERNAME = \'%s\' "%(code,username)
                     msg, res = statement.update_mysql(sql)
                     #发送邮件
                     sed = email.send_mail(username,code) 
                     if res == True and sed == True:
                         response_object['message'] = T
                         response_object['resCode'] = 101
                     else:
                         response_object['message'] = F
                 #如果生成新密码、更新数据库、发送邮件失败
                 else:  
                     response_object['message'] = F
         #如果该邮箱不合法
         else:
             response_object['message'] = vEmail
     else:
         response_object['message'] = "Unallowed request method."
     return jsonify(response_object)    
#注册api
@app.route('/api/register/',methods = ['POST', 'GET'])
def register():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username']
        xm = data['xm']
        password = data['password']
        code = data['code']
        #验证数据是否合法
        vEmail = validate.ValidateEmail(username)
        vXm = validate.ValidateXm(xm)
        vPs = validate.ValidatePassword(password)
        vCode = validate.ValidateCode(code)
        #判断邮箱是否获取过验证码
        idcode = ''
        if statement.Isgetsms(username) == True:
            idcode = statement.find_item('CODE','getsms',username)[0]
        else:
            idcode = email.get_code() #随机获取一个字符串
        #邮箱尚未注册
        if statement.Isregister(username) != True:
            #如果邮箱有效
            if vEmail == True:
                #如果昵称尚未被注册
                if statement.IsXmUsed(xm) != True:
                    #如果昵称有效
                    if vXm == True:
                        #如果密码有效
                        if vPs == True:
                            #如果验证码有效 and idcode == code
                            if vCode == True and code == idcode:
                                sql = "insert into register values (null,\'%s\',\'%s\',\'%s\',\'%s\')"%(username,xm,password,idcode)
                                msg, res = statement.insert_mysql(sql)
                                if res == True:
                                    response_object['message'] = "注册成功!"
                                    response_object['resCode'] = 101
                                else:
                                    response_object['message'] = "注册失败，请重新尝试！"
                            else:
                                response_object['message'] = "验证码不正确！"
                        #如果密码无效
                        else:
                            response_object['message'] = vPs
                    #如果昵称无效
                    else:
                        response_object['message'] = vXm
                #如果昵称已经被注册
                else:
                    response_object['message'] = "该用户名已存在，请重新尝试！"
            #如果邮箱无效
            else:
                response_object['message'] = vEmail
        #邮箱已注册
        else:
            response_object['message'] = "该邮箱账号已注册，请前往登录！"
    else:
         response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

#登录api
@app.route('/api/login/', methods = ['POST', 'GET'])
def login():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username']
        password = data['password']
        #验证邮箱是否已经注册
        #未注册
        if statement.Isregister(username) != True:
            response_object['message'] = "该邮箱账号尚未注册，请检查并重试！"         
        #已经注册
        else:
            #验证密码/验证码是否与register的匹配
            Ismatch_ps = False
            Ismatch_ps = statement.Ismatch('PASSWORD','register',username,password)
            #判断密码
            if Ismatch_ps == True:
              
                     xm = statement.find_item('XM','register',username)[0]
                     response_object['message'] = "登录成功！"
                     response_object['xm'] = xm
                     response_object['resCode'] = 101
            else:
                 response_object['message'] = "密码不正确，请重新尝试！"
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

#重置密码api
@app.route('/api/findps/', methods = ['POST', 'GET'])
def findps():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username']
        newpassword = data['password']
        code = data['code']
        #验证新密码是否合乎规范
        vPs = validate.ValidatePassword(newpassword)
        #验证邮箱是否已经注册
        #未注册
        if statement.Isregister(username) != True:
            response_object['message'] = "该邮箱账号尚未注册，请检查并重试！"         
        #已注册
        else:
            current_code = statement.find_item('CODE','register',username)[0]
            if code == current_code:
                if vPs == True:
                    sql = "UPDATE register SET  PASSWORD = \'%s\' WHERE USERNAME = \'%s\' "%(newpassword,username)
                    msg,res = statement.update_mysql(sql)
                    if res == True:
                        response_object['message'] = "密码重置成功！" 
                        response_object['resCode'] = 101
                    else:
                        response_object['message'] = "密码重置失败，请重试！" 
                else:
                    response_object['message'] = "无效密码，请重新输入！"
            else:
                response_object['message'] = "验证码不正确！" 
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

#意见反馈
@app.route('/api/addAdvice/', methods = ['POST', 'GET'])
def addAdvice():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        xm = data['xm']
        advice = data['advice']
        contact = data['contact']
        submitTime = data['submitTime']
        sql = "insert into addAdvice values (null,\'%s\',\'%s\',\'%s\',\'%s\')"%(xm,contact,advice,submitTime)
        msg,res = statement.insert_mysql(sql)
        if res == True:
            response_object['message'] = "提交成功，感谢您的反馈！" 
            response_object['resCode'] = 101
        else:
            response_object['message'] = "提交失败，请重试！"  
    else:
        response_object['message'] = "Unallowed request method."
    return jsonify(response_object)
   
###################################################################################################################(Cassie end)

#储存api
@app.route('/api/details/', methods = ['POST', 'GET'])
def addHabit():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username'].replace("\"","")
        title = data['title']
        habit_object = data['object']
        object_number = data['number']
        datetime = data['datetime']
        if statement.Ishabit(username,title) == True:
            response_object['message'] = "您已经创建过该习惯！请勿重复创建！"
        else:
            sql = "insert into habit values (null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(username,title,habit_object,object_number,datetime)
            print(sql)
            msg, res = statement.insert_mysql(sql)
            response_object['resCode'] = 101
            response_object['message'] = "Successful request"
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

#查询api
@app.route('/api/habit/', methods = ['POST', 'GET'])
def find_habit():
    response_object = {'status': 'success'}
    results = []
    datetime = ''
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        year = str(data['year'])
        if data['month'] >9:
            month = str(data['month'])
        else:
            month = "0" +str(data['month'])
        if data['date']>9:
            date = str(data['date'])
        else:
            date = "0" +str(data['date'])
        datetime = year + month +date
        sql = "select * from habit where username={} and datetime <={}".format(username,int(datetime))
        #print(sql)
        results = statement.find_mysql(sql)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['result'] = results
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

#查询api-inputDetail
@app.route('/api/inputDetail/', methods = ['POST','GET'])
def find_record():
    response_object = {'status':'success'}
    result=[]
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username'].replace("\"","")
        title = data['title']
        result = statement.find_records('STANDARD','DATE','inputDetail',username,title)
       # Xdata = statement.find_records('STANDARD','DATE','inputDetail',username,title)[1]
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['result'] = result
        #response_object['Xdata'] = Xdata
    else:
        response_object['message'] = "Unallowed request method."
    return jsonify(response_object)  

#insert每日打卡记录
@app.route('/api/GetDetail/', methods = ['POST', 'GET'])
def addrecord():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        #获取前端传来的数据
        data = request.get_json()
        username = data['username'].replace("\"","")
        title = data['title']
        standard = data['standard']
        date = data['date']
        attr = data['attr'][0]
        object_number = data['object_number']
        finished = ''
        if statement.Isdate(username,title,date) == True:
            sql2 = "DELETE FROM inputDetail WHERE username = '{}' and title = '{}' and date = '{}'".format(username,title,date)
            msg2 = statement.remove_mysql(sql2)
            print(msg2)
        else:
            response_object['message'] = "Successful request"
        if standard < object_number:
            finished = 'false'
        else:
            finished = 'true'
        print(finished)
        sql = "insert into inputDetail values (null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(username,title,attr,standard,date,finished)
        msg, res = statement.insert_mysql(sql)
        print(msg)
        response_object['resCode'] = 101
        response_object['message'] = "Successful request"
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

##查询完成情况
@app.route('/api/checkDetail/', methods = ['POST', 'GET'])
def check_habit():
    response_object = {'status': 'success'}
    results = []
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        datetime = data['datetime']
        sql = "select title,finished from inputDetail where username={} and date='{}' ".format(username,datetime)
        print(sql)
        results = statement.find_mysql(sql)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['result'] = results
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

##删除api
@app.route('/api/deleteDetail/', methods = ['POST', 'GET'])
def delete_habit():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        title = data['title']
        sql = "DELETE FROM habit WHERE username = {} and title = '{}'".format(username,title)
        sql2 = "DELETE FROM inputDetail WHERE username = {} and title = '{}'".format(username,title)
        print(sql)
        msg = statement.remove_mysql(sql)
        msg1 = statement.remove_mysql(sql2)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

##初始化api
@app.route('/api/showDetail/', methods = ['POST', 'GET'])
def show_habit():
    response_object = {'status': 'success'}
    datetime = ''
    results=[]
    if request.method == 'GET':
        username = request.args.get("username")
        datetime = request.args.get("datetime")
        sql = "select * from habit where username={} and datetime <={}".format(username,int(datetime))
        results = statement.find_mysql(sql)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['result'] = results
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

##初始化api2
@app.route('/api/checkDetail1/', methods = ['POST', 'GET'])
def check_habit1():
    response_object = {'status': 'success'}
    datetime = ''
    results=[]
    if request.method == 'GET':
        username = request.args.get("username")
        datetime = request.args.get("datetime")
        sql = "select title,finished from inputDetail where username={} and date ={}".format(username,datetime)
        results = statement.find_mysql(sql)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['result'] = results
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)

##初始化api3
@app.route('/api/checkDetail2/', methods = ['POST', 'GET'])
def check_habit2():
    response_object = {'status': 'success'}
    datetime = ''
    inputDetail_results = []
    habit_results = []
    if request.method == 'GET':
        username = request.args.get("username")
        sql = "select date,finished from inputDetail where username={}".format(username)
        sql2 = "select title,datetime,habit_object,object_number from habit where username={}".format(username)
        inputDetail_results = statement.find_mysql(sql)
        habit_results = statement.find_mysql(sql2)
        response_object['message'] = "Successful request"
        response_object['resCode'] = 101
        response_object['inputDetail_result'] = inputDetail_results
        response_object['habit_result'] = habit_results
    else:
          response_object['message'] = "Unallowed request method."
    return jsonify(response_object)


###################################################################################################################(Sammy end)

if __name__=='__main__':
    #df1 = pd.read_excel("test.xlsx")
    app.run(debug=True)
