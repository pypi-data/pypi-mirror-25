# -*- coding:utf-8 -*-
from packages.md5 import MD5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
    创建时间：2016-4-19
    创建人：王鑫
'''

class LoginSign(object):
    """
    appid='1020140422102642'
    key='d10de75498ae82987f08d3653b092cc7'
    time=str(int(time.time()*1000)) #13位时间戳，与java里一致

    server=''
    userAccount=''
    password=''
    deviceId=''
    def __init__(self,server,userAccount,password,deviceId):
        self.server=server
        self.userAccount=userAccount
        self.password=password
        self.deviceId=deviceId


    def pawmd5(self):
        t=self.time
        #print t
        m=MD5(self.password,t,'UTF-8')
        return m.sign_pwd()

    def datamd5(self):
        data=self.userAccount+"|1| |"+self.pawmd5()+"|"+self.deviceId+"|"+"15"+"|"+ " | "
        test=self.server+"&"+self.appid+"&"+self.time+"&"+data
        m=MD5(test,self.key,"UTF-8")
        return self.time,m.sign_data(),data
    """

    key="d10de75498ae82987f08d3653b092cc7"#key为固定不变

    #获取密码的MD5值
    def pawmd5(self,password,time):
        '''把登录时候的密码按MD5加密的方式返回
         | pawmd5                   | passwork,time              |
        '''
        m=MD5(password,time)
        return m.sign_pwd()

    #获取数据的MD5值
    def datamd5(self,text):
        '''把登录时候的报文按MD5加密的方式返回(text具体参数见接口文档)
         | datamd5                   | text              |
        '''
        m=MD5(text,self.key)
        return m.sign_data()

#print LoginSign().datamd5('service=innotek.public.login.v2.0&app_id=1020140422193618&req_time=1461141002283&data=15305712196|1||1f36ceeb0b8ff1843213fabd7b2e2855|TEST-WX|10||4.0')