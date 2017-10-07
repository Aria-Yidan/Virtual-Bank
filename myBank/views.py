# -*- coding:UTF-8 -*-
import time
import hashlib
import base64
#import md5
#import os
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from myBank.models import UnactivationUser,BankUser,Account,TransactionRecord
from myBank.RSA import *
from Crypto.Cipher import AES
import rsa

#from PIL import Image,ImageDraw,ImageFont
#from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# Define global variable--#
HOMEPAGE_URL = "http://127.0.0.1:8000/"
SHOPHOMEPAGE_URL = "http://127.0.0.1:8000/"
HOMEEMAIL = 'virtualbankbylcl@sina.com'
TransactionState = {-1:u"交易失败", 0:u"交易进行中", 1:u"交易成功"}
TransactionType = {"income":True, "pay":False}
TransactionName = {"transferin":u"转入", "transferout":u"转出", "save":u"存入", "withdrew":u"取出", "buy":u"购买"}
PADDING = '\0'
pad_it = lambda s: s+(16 - len(s)%16)*PADDING 


#-----------------------HTML Fuction-------------------------------------------
 #--RSA project e--#
#rsa = getRSA()
#rsa_key = RSAKeyPair("10001","367fbdde3df00db317f914949dd02b01","94b8c162b498f08d139461950b4f3851")
rsa_key = RSAKeyPair("10001","59a4d41533777950f9580b6c1bd1c78abc1a597429e27901bd475a9abeccde7450132d73224bb3747f98bec9704be7b9265bba8dba5b27a6b57fdbbdf1525881","92ec287fefb11b13c7bebab2ce2572b59961afbf2e5c8ddf185aa7184e0df5273987909aabb005d9dea46b01c1d9de0bad336363ad607679411cd8fd24ceb609")
rsa_sign_key = RSAKeyPair("10001","6f01044204c8765c13599ff8b104b3457cb612dd52688e163964765a6fb275b59e7b8c5719388ad0460b9bbb4ed7bac5caca121724b94c406fbd47b5ea0635f1","a8924727773326f6dffa3ae80459b7802774f3c0b9ae857c5acc7c3b8b9f8588a81212bb69f5d1c687de1b08fdd09df093d40550a0d934e7ea7ced223b645165")
rsa_key_e = "10001"
rsa_key_d = "59a4d41533777950f9580b6c1bd1c78abc1a597429e27901bd475a9abeccde7450132d73224bb3747f98bec9704be7b9265bba8dba5b27a6b57fdbbdf1525881"
rsa_key_n = "92ec287fefb11b13c7bebab2ce2572b59961afbf2e5c8ddf185aa7184e0df5273987909aabb005d9dea46b01c1d9de0bad336363ad607679411cd8fd24ceb609"
def homepage(request):
    try:
        BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    return render_to_response('VirtualBank_homepage.html',locals())

def register(request):
    error = []
    #--get RSA e--#
    #rsa_e = "10001"
    #rsa_n = "94b8c162b498f08d139461950b4f3851"
    #captcha=CaptchaField()
    if request.POST:
        post = request.POST
        
        """
        #--test1 移位加密--#
        key_encrypted = int(post["key_encrypted"])
        key = pow(key_encrypted, rsa['d'], rsa['n'])
        username_c = post["username"]
        username = []
        for i in range(len(username_c)):
            username.append(chr(ord(username_c[i]) - key))
        username = ''.join(username)
        """
        key_encrypted = post["key_encrypted"]
        iv_encrypted = post["iv_encrypted"]
        password_encrypted = post["password_encrypted"]
        email_encrypted = post["email_encrypted"]
        get_checksum = post["checksum"]
        hash_checksum = hashlib.md5()
        hash_checksum.update(key_encrypted + iv_encrypted + password_encrypted + email_encrypted)
        checksum = hash_checksum.hexdigest()
        if (checksum == get_checksum):
            
            #--Must different username--#
            username = post["username"]
            try:
                User.objects.get(username=username)
                error.append("用户名已存在！")
                return render_to_response('VirtualBank_register3.html',locals())
            except:
                pass
            
            #--Decrypt the key_encrypted--#
            key = decryptedString(rsa_key,key_encrypted)
            iv = decryptedString(rsa_key,iv_encrypted)
            
            #--Decrypt the email_encrypted--#
            email_encrypted = base64.b64decode(email_encrypted)
            generator = AES.new(key, AES.MODE_CBC, iv)
            email = generator.decrypt(email_encrypted)
            email = email.rstrip(PADDING)
            
            #--Decrypt the password_encrypted--#
            password_encrypted = base64.b64decode(password_encrypted)
            generator = AES.new(key, AES.MODE_CBC, iv)
            password = generator.decrypt(password_encrypted)
            password = password.rstrip(PADDING)
            
            #--deal with password by using MD5--#
            hash_password = hashlib.md5()
            hash_password.update(password)
            password_save = hash_password.hexdigest()
            
            #--Create a new django.contrib.auth.models.User--#
            user = User.objects.create_user(username=username,password=password_save)
            newID = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randrange(1000,9999))
            
            #--Create a new UnactivationUser--#
            random_actCode = hex(random.randrange(2**32,2**33))
            hash_actCode = hashlib.md5()
            hash_actCode.update(newID + password_save + random_actCode)
            actCode = hash_actCode.hexdigest()
            UnactivationUser.objects.create(
                UserID = newID,
                Password = password_save,
                Userinf = user,
                Email = email,
                ActivationCode = actCode
            )

            #--Send activation email--#
            user_email = email
            activationURL = HOMEPAGE_URL+'activation/'+newID+'$$'+actCode+'/'
            
            subject,form_email,to = u'欢迎使用财富管家', HOMEEMAIL, user_email
            text_content = u'欢迎您，尊敬的 ' + username + '\n'
            html_content = u'<h1>'+u'欢迎您，尊敬的 ' + username+u'</h1><h3>您已经成功注册了财富管家账户，请点击下面的链接，进行账户激活然后正常登录！</h3><h3>激活链接：<a href="'+activationURL+'">'+activationURL+'</a></h3>'
            msg = EmailMultiAlternatives(subject,text_content,form_email,[to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            #send_mail(send_title, send_message, HOMEEMAIL, [user_email], fail_silently=True)
        else:
            error.append("信息校验错误，请重新输入")
        
        return HttpResponseRedirect(HOMEPAGE_URL+'login')
                    
    return render_to_response('VirtualBank_register3.html',locals())    

def activation(request,offset):
    error = []
    inf = offset.split("$$")
    try:
        unactu = UnactivationUser.objects.get(UserID = inf[0])
        if (unactu.ActivationCode == inf[1]):
            #--Create a new empty Account--#
            new_Account = Account.objects.create(
                UserID = unactu.UserID,
                Balance = 0.00,
                Payword = ""
            )
            
            #--Create a new BankUser--#
            BankUser.objects.create(
                UserID = unactu.UserID,
                ActivationType = True,
                Password = unactu.Password,
                Userinf = unactu.Userinf,
                Email = unactu.Email,
                Account = new_Account
            )
            #--Delete the unuseful UnactivationUser--#
            UnactivationUser.objects.get(UserID = inf[0]).delete()
        else:
            error.append("无法激活，无效的激活码")
    except:
        error.append("无法激活，无法确认用户身份")
    
            
    return render_to_response('VirtualBank_activation.html',locals())

def login(request):
    error = []
    
    if request.POST:
        post = request.POST
        try:
            userb = User.objects.get(username = post['username'])
            try:
                bu = BankUser.objects.get(Userinf = userb)
                get_password = post['password']
                get_salt = post['salt']
                
                #--Check password--#
                hash_check = hashlib.md5()
                hash_check.update(bu.Password + get_salt)
                check_password = hash_check.hexdigest()
                
                if (check_password == get_password):
                    user = auth.authenticate(username=post["username"], password=bu.Password)
                    if user:
                        auth.login(request, user)
                    else:
                        error.append("User类错误！")
                        return render_to_response('VirtualBank_login.html',locals())
                    return HttpResponseRedirect(HOMEPAGE_URL)
                else:
                   error.append("密码错误！")
            except:
                unactu = UnactivationUser.objects.get(Userinf = userb)
                error.append("请到注册邮箱中激活您的账户")
        except:
            error.append("用户不存在！")
    return render_to_response('VirtualBank_login.html',locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(HOMEPAGE_URL)   
    
def querybalance(request):
    try:
        BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    bal = 0
    
    user_balance = None
    if (userflag == True):
        bu = BankUser.objects.get(Userinf = request.user)
        user_balance = bu.Account.Balance
        
        #--encrypt the balance--#        
        
        return render_to_response('VirtualBank_querybalance.html',locals())
        
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def querybill(request):
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    user_TransactionRecords = []
    if (userflag == True):
        
        TransactionRecords = TransactionRecord.objects.filter(Account = bu.Account)
        TransactionRecords = list(TransactionRecords)
        
        #--make the infirmation--#
        for tempTR in TransactionRecords:
            tempList = []
            tempList.append(tempTR.Date)
            tempList.append(tempTR.TransactionName)
            tempList.append(BankUser.objects.get(UserID = tempTR.AnotherAccountID).Userinf.username)
            if (tempTR.Type):
                tempList.append('+' + tempTR.Money)
            else:
                tempList.append('-' + tempTR.Money)
            #tempList.append(tempTR.TransactionID)
            tempList.append(tempTR.State)
            
            user_TransactionRecords.append(tempList)
        
        #--Encrypt these information--#
        
        
        return render_to_response('VirtualBank_querybill.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')
    
def payset(request):
    try:
        BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username

    if (userflag == True):
        return render_to_response('VirtualBank_payset.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def setpassword(request):
    error = []
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    passflag = False
    user_Challenge = None
    if (userflag == True):
        if request.POST:
            post = request.POST
            if "proving" in post:
                get_response = post["response"]
                
                #--Check the oldpassword--#
                checkChallenge = bu.Random
                hash_checkChallenge = hashlib.sha1()
                hash_checkChallenge.update(bu.Password + checkChallenge)
                checkResponse = hash_checkChallenge.hexdigest()
                if (checkResponse == get_response):
                    passflag = True
                else:
                    passflag = False
                    error.append("原密码错误！")
                
            elif "changing" in post:
                get_newpassword = post["newpassword"]
                
                #--Descrypt the get_newpassword--#
                newpassword = get_newpassword
                
                #--Update the password--#
                hash_newpassword = hashlib.md5()
                hash_newpassword.update(newpassword)
                bu.Password = hash_newpassword.hexdigest()
                bu.save()
                bu.Userinf.set_password(bu.Password)
                bu.Userinf.save()
                
                auth.logout(request)
                return HttpResponseRedirect(HOMEPAGE_URL+'login')
        #--Create a new challenge--#
        random_challenge = str(random.randrange(2**128,2**132))
        hash_challenge = hashlib.sha1()
        hash_challenge.update(random_challenge)
        user_Challenge = hash_challenge.hexdigest()
        bu.Random = user_Challenge
        bu.save()
        return render_to_response('VirtualBank_setpassword.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def setpayword(request):
    error = []
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username

    passflag = False
    if (userflag == True):
        ac = bu.Account

        if request.POST:
            post = request.POST
            
            if "IDproving" in post:
                get_response = post["response"]
            
                #--Check the oldpassword--#
                checkChallenge = ac.Challenge
                hash_checkChallenge = hashlib.sha1()
                hash_checkChallenge.update(ac.Payword + checkChallenge)
                checkResponse = hash_checkChallenge.hexdigest()
                if (checkResponse == get_response):
                    passflag = True
                else:
                    passflag = False
                    error.append("支付密码错误！")
            elif "setnewpassword" in post:
                get_newpayword = post["newpayword"]
                
                #--Descrypt the get_newpayword--#
                newpayword = get_newpayword
                
                #--Update the payword--#
                hash_newpayword = hashlib.sha1()
                hash_newpayword.update(newpayword)
                ac.Payword = hash_newpayword.hexdigest()
                ac.save()
                passflag = False
                return HttpResponseRedirect(HOMEPAGE_URL)
                
        #--New BankUser set payword first--#
        if (ac.Payword == ""):
            passflag = True
            
        
        #--Create a new challenge--#
        random_challenge = str(random.randrange(2**128,2**132))
        hash_challenge = hashlib.sha1()
        hash_challenge.update(random_challenge)
        user_Challenge = hash_challenge.hexdigest()
        ac.Challenge = user_Challenge
        ac.save()
        return render_to_response('VirtualBank_setpayword.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def myaccount(request):
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    changeflag = False
    
    if (userflag == True):
        
        if (request.POST):
            post = request.POST
            if "reqchange" in post:
                changeflag = True
                user_phone = bu.Phone
                return render_to_response('VirtualBank_myaccount.html',{"userflag":userflag,"user_name":user_name,"changeflag":changeflag,"user_phone":user_phone})
            
            #--Decrypt the information changed--#
            get_username = post["username"]
            get_userphone = post["userphone"]
            
            user = bu.Userinf
            user.username = get_username
            user.save()
            bu.Phone = get_userphone
            bu.save()
            
        
        user_id = bu.UserID
        user_email = bu.Email
        user_phone = bu.Phone
        user_name = bu.Userinf.username
        return render_to_response('VirtualBank_myaccount.html',{"userflag":userflag,"user_name":user_name,"changflag":changeflag,"user_id":user_id,"user_email":user_email,"user_phone":user_phone})
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def newTransactionRecord(TransactionTime, trName, trType, trMoney, AnotherAccountID, Account, State):
    #--make a new TransactionRecordID--#
    hash_id = hashlib.sha1()
    hash_id.update(Account.UserID)
    hash_id.update(AnotherAccountID)
    hash_id.update(TransactionTime)
    newTransactionID = TransactionTime + hash_id.hexdigest()
    
    #Create a new TransactionRecord--#
    TR = TransactionRecord.objects.create(
        TransactionID = newTransactionID,
        Date = TransactionTime[:-10] + '-' + TransactionTime[-10:-8] + '-' + TransactionTime[-8:-6] ,
        TransactionName = trName,
        Type = trType,
        Money = str(trMoney),
        AnotherAccountID = AnotherAccountID,
        Account = Account,
        State = State
    )
    
    return TR

def transfer(request):
    error = []
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    IDprovingflag = False
    if (userflag == True):
        if (bu.Account.Payword == ""):
            return HttpResponseRedirect(HOMEPAGE_URL + 'payset/set-payword' )
        
        if request.POST:
            post = request.POST
            if "needIDproving" in post:
                #--Decrypt transfer infromation--#
                
                #--Search aimAccount--#
                try:
                    aimuser = User.objects.get(username = post["trAccount"])
                    aimbu = BankUser.objects.get(Userinf = aimuser)
                    get_trAccount = aimbu.Account
                except:
                    try:
                        aimbu = BankUser.objects.get(UserID = post["trAccount"])
                        get_trAccount = aimbu.Account
                    except:
                        error.append("账号输入错误！")
                        return render_to_response('VirtualBank_transfer.html',locals())
                get_trMoney = post["trMoney"]
        
                trAccount = get_trAccount
                trMoney = get_trMoney
                
                #--Create a new TransactionRecord--#
                TransactionTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                TR = newTransactionRecord(TransactionTime, TransactionName["transferout"], TransactionType["pay"], trMoney, trAccount.UserID, bu.Account, TransactionState[0])
                user_TransactionID = TR.TransactionID
                hash_checksum = hashlib.sha1()
                hash_checksum.update(user_TransactionID)
                hash_checksum.update(user_name)
                user_TransactionID_CheckSum = hash_checksum.hexdigest()
                
                #--Create a new Challenge--#
                IDprovingflag = True
                random_challenge = str(random.randrange(2**128,2**132))
                hash_challenge = hashlib.sha1()
                hash_challenge.update(random_challenge)
                user_Challenge = hash_challenge.hexdigest()
                bu.Account.Challenge = user_Challenge
                bu.Account.save()
                return render_to_response('VirtualBank_transfer.html',
                                          {"userflag":userflag,"user_name":user_name,"IDprovingflag":IDprovingflag,"user_TransactionID":user_TransactionID,"user_Challenge":user_Challenge,"user_TransactionID_CheckSum":user_TransactionID_CheckSum})
            else:#--IDproving--#
                get_response = post["response"]
                get_transactionID = post["transactionID"]
                get_transactionID_CheckSum = post["transactionID_CheckSum"]
                
                #--Decrypt get_transactionID--#
                transactionID = get_transactionID
                
                #--Check TransactionID_CheckSum--#
                hash_checksum = hashlib.sha1()
                hash_checksum.update(transactionID)
                hash_checksum.update(user_name)
                if (get_transactionID_CheckSum != hash_checksum.hexdigest()):
                    error.append("账号身份错误！")
                    return render_to_response('VirtualBank_transfer.html',locals())
                
                #--Check response--#
                try:
                    TR = TransactionRecord.objects.get(TransactionID = transactionID)
                    checkChallenge = TR.Account.Challenge
                    hash_checkChallenge = hashlib.sha1()
                    hash_checkChallenge.update(TR.Account.Payword + checkChallenge)
                    checkResponse = hash_checkChallenge.hexdigest()
                    if (checkResponse == get_response):
                        if (float(bu.Account.Balance) > float(TR.Money)):
                            #--Deduct money--#
                            bu.Account.Balance = str(round(float(bu.Account.Balance) - float(TR.Money),2))
                            bu.Account.save()
                            #--Change TransactionState--#
                            TR.State = TransactionState[1]
                            TR.save()
                            #--Remit account--#
                            aimAccount = Account.objects.get(UserID = TR.AnotherAccountID)
                            aimAccount.Balance += TR.Money
                            aimAccount.save()
                            #--Create a new TransactionRecord
                            TransactionTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                            newTransactionRecord(TransactionTime, TransactionName["transferin"], TransactionType["income"], TR.Money, bu.Account.UserID, aimAccount, TransactionState[1])
                            
                            error.append("交易成功！")
                        else:
                            error.append("余额不足！")
                            return render_to_response('VirtualBank_transfer.html',locals())
                    else:
                        error.append("支付密码错误！")
                        #--Change TransactionState--#
                        TR.State = TransactionState[-1]
                        TR.save()
                except:
                    error.append("交易错误！")
                    
                return render_to_response('VirtualBank_transfer.html',locals())
            
            
        return render_to_response('VirtualBank_transfer.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')
        
def saveorwithdrew(request):
    try:
        BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    if (userflag == True):
        return render_to_response('VirtualBank_saveorwithdraw.html',locals())
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def saveorwithdrew_save(request):
    error = []
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    user_Challenge = None
    #savesuccess = False
    
    if (userflag == True):
        if request.POST:
            post = request.POST
            if "savepost" in post:
                
                get_saveMoney = post["saveMoney"]
                
                #--Decrypt the saveMoney--#
                
                saveMoney = get_saveMoney
                
                #--IDproving--#
                get_response = post["response"]
                checkChallenge = bu.Account.Challenge
                hash_checkChallenge = hashlib.sha1()
                hash_checkChallenge.update(bu.Account.Payword + checkChallenge)
                checkResponse = hash_checkChallenge.hexdigest()
                if (checkResponse == get_response):
                    #--Change user's balance--#
                    ac = bu.Account
                    ac.Balance = str(float(ac.Balance) + float('%0.2f'%float(saveMoney)))
                    if (ac.Balance[-2] == '.'):
                        ac.Balance += '0'
                    ac.save()
                    #savesuccess = True
                    
                    
                    #--Create a new TransactionRecord--#
                    TransactionTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                    TR = newTransactionRecord(TransactionTime, TransactionName["save"], TransactionType["income"], saveMoney, bu.Account.UserID, bu.Account, TransactionState[1])
                    """
                    user_TransactionID = TR.TransactionID
                    hash_checksum = hashlib.sha1()
                    hash_checksum.update(user_TransactionID)
                    hash_checksum.update(user_name)
                    user_TransactionID_CheckSum = hash_checksum.hexdigest()
                    """
                    return HttpResponseRedirect(HOMEPAGE_URL+ 'querybalance')
                else:
                    error.append("支付密码错误")
                
        #--Create a new Challenge--#
        random_challenge = str(random.randrange(2**128,2**132))
        hash_challenge = hashlib.sha1()
        hash_challenge.update(random_challenge)
        user_Challenge = hash_challenge.hexdigest()
        bu.Account.Challenge = user_Challenge
        bu.Account.save()
                
        return render_to_response('VirtualBank_saveorwithdraw_save.html',locals())
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def saveorwithdraw_withdrew(request):
    error = []
    try:
        bu = BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username

    user_Challenge = None
    if (userflag == True):
        if request.POST:
            post = request.POST
            if "withdrewpost" in post:
                
                get_withdrewMoney = post["withdrewMoney"]
                
                #--Decrypt the saveMoney--#
                
                withdrewMoney = get_withdrewMoney
                
                #--IDproving--#
                get_response = post["response"]
                checkChallenge = bu.Account.Challenge
                hash_checkChallenge = hashlib.sha1()
                hash_checkChallenge.update(bu.Account.Payword + checkChallenge)
                checkResponse = hash_checkChallenge.hexdigest()
                if (checkResponse == get_response):
                    ac = bu.Account
                    if (float(ac.Balance) < float(withdrewMoney)):
                        error.append("余额不足")
                    #--Change user's balance--#
                    ac.Balance = str(round(float(ac.Balance) - float(withdrewMoney),2))
                    if (ac.Balance[-2] == '.'):
                        ac.Balance += '0'
                    ac.save()

                    #--Create a new TransactionRecord--#
                    TransactionTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                    TR = newTransactionRecord(TransactionTime, TransactionName["withdrew"], TransactionType["pay"], withdrewMoney, bu.Account.UserID, bu.Account, TransactionState[1])
                    """
                    user_TransactionID = TR.TransactionID
                    hash_checksum = hashlib.sha1()
                    hash_checksum.update(user_TransactionID)
                    hash_checksum.update(user_name)
                    user_TransactionID_CheckSum = hash_checksum.hexdigest()
                    """
                    return HttpResponseRedirect(HOMEPAGE_URL+ 'querybalance')
                else:
                    error.append("支付密码错误")
                
        #--Create a new Challenge--#
        random_challenge = str(random.randrange(2**128,2**132))
        hash_challenge = hashlib.sha1()
        hash_challenge.update(random_challenge)
        user_Challenge = hash_challenge.hexdigest()
        bu.Account.Challenge = user_Challenge
        bu.Account.save()
        return render_to_response('VirtualBank_saveorwithdraw_withdraw.html',locals())
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def newmessage(request):
    try:
        BankUser.objects.get(Userinf = request.user)
        userflag = True
    except:
        userflag = False
    user_name = request.user.username
    
    if (userflag == True):
        
    
    
        return render_to_response('VirtualBank_saveorwithdraw.html',locals())
    
    return HttpResponseRedirect(HOMEPAGE_URL+'login')

def cashierdesk(request,offset):
    #http://127.0.0.1:8000/cashierdesk/shopid=201605052143358660$$payOrderID=102010201$$payMoney=100
    error = []
    
    aimaction = None
    cashierdesk_result = None
    if request.POST:
        post = request.POST
        
        #--Get BankUser--#
        username = post["username"]
        try:
            ur = User.objects.get(username = username)
            bu = BankUser.objects.get(Userinf = ur)
            
            shopid = post["shopid"]
            payOrderID = post["payOrderID"]
            payMoney = post["payMoney"]
            
            #--Check the payword--#
            inpayword = post["inpayword"]
            t = hashlib.sha1()
            t.update(inpayword)
            if ( t.hexdigest() == bu.Account.Payword):
                ac = bu.Account
                if (float(ac.Balance) < float(payMoney)):
                    error.append("余额不足")
                else:
                    #--Change user's balance--#
                    ac.Balance = str(round(float(ac.Balance) - float(payMoney),2))
                    if (ac.Balance[-2] == '.'):
                        ac.Balance += '0'
                    ac.save()
                    
                     #--Create a new TransactionRecord--#
                    TransactionTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                    TR = newTransactionRecord(TransactionTime, TransactionName["buy"], TransactionType["pay"], payMoney, shopid, bu.Account, TransactionState[1])
                    
                    #--Return th result--#
                    aimaction = SHOPHOMEPAGE_URL+'payresult/'+'payOrderID='+payOrderID+'$$'+'needtocheck'
                    cashierdesk_result = "success"
                    #return HttpResponseRedirect(SHOPHOMEPAGE_URL+'payresult/'+'payOrderID='+payOrderID+'$$'+'result=success')
        except:
            error.append("无效的用户名")
    #--Decrypt information from URL--#
    
    
    #--deal with information--#
    try:
        inf = offset.split("$$")
        if ('shopid=' in inf[0]):
            shopid = inf[0][7:]
        
        if ('payOrderID=' in inf[1]):
            payOrderID = inf[1][11:]
        if ('payMoney=' in inf[2]):
            payMoney = inf[2][9:]
        
        try:
            shop = BankUser.objects.get(UserID = shopid)
            shopname = shop.Userinf.username
            shopid = shop.UserID
        except:
            error.append("无效的商家ID")
    except:
        error.append("无效的链接")
    #--Create 
    return render_to_response('VirtualBank_cashierdesk.html',locals())
#-----------------------------------------------------------------------------#
"""
def get_check_code_image(request):
    
    im_name_list = ['validata_code1.jpg', 'validata_code2.jpg', 'validata_code3.jpg', 'validata_code4.jpg','validata_code5.jpg', 'validata_code6.jpg', 'validata_code7.jpg', 'validata_code8.jpg']
    
    im_path = os.path.join('medias','common_img')
    im_name = os.path.join(im_path, im_name_list[random.randint(0, 7)])
    
    im = Image.open(im_name)
    draw = ImageDraw.Draw(im)
    
    mp = md5.new()
    mp_src = mp.update(str(datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:4]
    
    draw.text((5,0), rand_str[0], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,35)))
    draw.text((20,0), rand_str[1], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,35)))
    draw.text((35,0), rand_str[2], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,35)))
    draw.text((50,0), rand_str[3], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,35)))
    del draw
        
    request.session['identify_code'] = rand_str
    buf = cStringIO.StringIO()
    im.save(buf, 'png')
    
    return HttpResponse(buf.getvalue(),'image/png')
"""
def test(request):
#    (pub,pri) = rsa.newkeys(512)
#    VirtualBank_RSA_pub = pub.n
    
    return render_to_response('VirtualBank_test.html',locals())