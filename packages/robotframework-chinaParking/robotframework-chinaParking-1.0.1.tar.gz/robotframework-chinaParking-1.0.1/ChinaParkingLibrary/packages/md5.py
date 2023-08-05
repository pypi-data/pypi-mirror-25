# -*- coding:utf-8 -*-
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MD5:
  text = ""
  key = ""

  def __init__(self,text,key):
    self.text = text
    self.key = key

  def get_digest(self):
      return hashlib.md5(self.text).hexdigest()

  #data内容MD5加密
  def sign_data(self):
      self.text=self.text+"&"+self.key
      return self.get_digest()

  #密码MD5加密
  def sign_pwd(self):
    self.text=self.text+"&key="+self.key
    return self.get_digest()

#m=MD5('innotek.public.bind.licenseplate.v2.2&1020140422102642&1461582674503&95ec0168-9cf5-45f2-b47c-fa7e7e9e|93e7b18b-5cc3-49a0-9915-043e2da73f45|1|浙A12345|1|0|2',"d10de75498ae82987f08d3653b092cc7")
#print m.sign_data()