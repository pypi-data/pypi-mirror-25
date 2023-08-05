# -*- coding:utf-8 -*-
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#MD5加密
def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

#SHA1加密
def get_sha1_value(src):
    mySha1 = hashlib.sha1()
    mySha1.update(src)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest