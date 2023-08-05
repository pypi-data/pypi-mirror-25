# -*- coding:utf-8 -*-
import time
import base64
from Crypto.Cipher import AES
from packages.mailtools import base_send_mail


class Tools(object):
    def getreqtime(self):
        '''获取当前的13位的时间戳
         | get13time |
        '''
        return str(int(time.time()*1000)) #13位时间戳，与java里一致

    def str2base64(self,str):
        '''把字符串作base64编码
         | string |
        '''
        return base64.encodestring(str)

    def base64Tostr(self,base64_str):
        '''把base64串解码
         | base64_str |
        '''
        return base64.decodestring(base64_str)

    def list2dict(self,list1,list2):
        '''把两个list合并成dict，一一对应
         | list1 | list2 |
        ''' 
        return dict(zip(list1,list2))

    def aes_encryt(self,str, key):
        '''AES加密并进行BASE64编码后得到的密文(AES_MODE为ECB)
            str:要加密的字符串
            key：加密秘钥
               | str | key |
        '''
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(key, AES.MODE_ECB, str)
        msg = cipher.encrypt(pad(str))
        msg = base64.encodestring(msg)
        return msg

    def aes_decrypt(self,enStr, key):
        '''解密通过AES加密并进行BASE64编码后的密文(AES_MODE为ECB)
            enStr:已加过密的密文
            key：加密秘钥
                | enStr | key |
        '''
        unpad = lambda s: s[0:-ord(s[-1])]
        cipher = AES.new(key, AES.MODE_ECB)
        decryptByts = base64.decodestring(enStr)
        msg = cipher.decrypt(decryptByts)
        msg = unpad(msg)
        return msg

    def send_mail(self,to_addr,header,to_data):
        '''
        发送邮件
        to_addr:收件人邮箱地址,多个地址之间用逗号(,)隔开
        header:邮件标题
        to_data：邮件内容
        | to_addr | header | to_data |

        '''
        return base_send_mail(to_addr,header,to_data)




