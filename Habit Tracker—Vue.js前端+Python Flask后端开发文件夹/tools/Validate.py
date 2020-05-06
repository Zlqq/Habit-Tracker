import re

def ValidateEmail(value):    
    reg = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
    match = re.search(reg,value)
    if value == '':
        return "Email address can't be empty."
    elif match == None :
        return "Invalid email address."
    else:
        return True

def ValidateXm(value):
    reg = r'^^[\u4E00-\u9FA5A-Za-z0-9]{3,8}$'
    match = re.search(reg,value)
    if value == '':
        return "Username can't be empty."
    elif match == None :
        return "Invalid username."
    else:
        return True
        
def ValidatePassword(value):
    reg = r'^(?!\D+$)(?![^a-zA-Z]+$)\S{6,20}$'
    match = re.search(reg,value)
    if value == '':
        return "Password can't be empty."
    elif match == None :
        return "Invalid password."
    else:
        return True    
        
def ValidateCode(value):
    reg = r'^[0-9A-Za-z]{6}$'
    match = re.search(reg,value)
    if value == '':
        return "Vertification code can't be empty."
    elif match == None :
        return "Invalid vertification code."
    else:
        return True
    #return True if match!= None else False


