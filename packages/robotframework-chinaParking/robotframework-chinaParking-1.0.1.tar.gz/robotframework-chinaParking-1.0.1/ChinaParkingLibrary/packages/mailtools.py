# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def base_send_mail(to_addr,header,to_data):
    #from_addr = '30329128@qq.com'
    #password = 'sjxqiiutsnkmbhhc' #现在的邮箱都要授权码,开通smtp后获取授权码,用授权码登录即可
    from_addr = '1822180559@qq.com'
    password ='ikkysqmnkxmvcded'
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(to_data, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'创泰测试<%s>' % from_addr)
    msg['To'] = to_addr  # 收件人必须是字符串
    #msg['To'] = ','.join(to_addr)#收件人必须是字符串
    to_addr = to_addr.split(',')#发送时必须是list

    print to_addr
    msg['Subject'] = Header(header, 'utf-8').encode()

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)  # 必须用ssl协议登录
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        return "Success!"
    except smtplib.SMTPException, e:
        return "Falied,%s" % e