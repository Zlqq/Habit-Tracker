# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText  #发送文本
from email.header import Header
import random
from random import shuffle

#随机生成验证码
def get_code():
    code = ""
    l = str(random.choice([chr(random.randint(97, 122)),chr(random.randint(65, 90))])) #至少1位字母
    n = str(random.randint(0, 9))#至少一位数字
    code_part = ''
    for i in range(4):
        num = random.randint(0, 9)
        letter = chr(random.randint(97, 122))#取小写字母
        Letter = chr(random.randint(65, 90))#取大写字母
        s = str(random.choice([num,letter,Letter]))
        code_part += s
    code = shuffle_str(l + n + code_part)
    return code
#print(get_code())

def shuffle_str(s):
    # 将字符串转换成列表
    str_list = list(s)
    # 调用random模块的shuffle函数打乱列表
    shuffle(str_list)
    # 将列表转字符串
    return ''.join(str_list)

#发送邮件
def send_mail(receiver,code):
    sed = False
    try:
        #第三方SMTP服务
        mail_host = 'smtp.qq.com'  #SMIP服务器
        mail_user = '1295057620@qq.com' 
        mail_pass = 'etrvukbhzpdmbaee' 
        #发件人
        sender = '1295057620@qq.com'
        #邮件主题
        title = "验证码"
        content = """
        <hr>
        <h2> 【Habit Tracker】验证码: <span style="color:red;">{}</span></h2>
        <p>为了您的账号安全，请勿泄露给他人。（若非本人操作，请忽略本邮件）<p>
        <hr>
        """.format(code)
        ##############################################
        #1 搭建SMTP服务器
        email_server = smtplib.SMTP() # SMTP服务器
        email_server.connect(mail_host,25)
        #2 发件人登录
        email_server.login(mail_user, mail_pass) # 发件人登录
        #3 Create msg
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = Header(title, 'utf-8') #邮件的主题，也可以说是标题
        msg['From'] = sender
        msg['To'] =  receiver
        #4 发送邮件
        email_server.sendmail(sender,receiver,msg.as_string()) 
        print("邮件发送成功")
        sed = True
        #5 关闭服务器
        email_server.quit()  # 关闭连接
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")  
        sed = False
    return sed
#send_mail(receiver ,code)