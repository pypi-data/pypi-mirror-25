# -*- coding:utf-8 -*-
from datetime import datetime


# 判断date是星期几(1,2,3,4,5,6,7),周末返回0,非周末返回1
def isworkday(date):
    work = 1
    dayOfWeek = date.weekday() + 1
    if dayOfWeek == 6 or dayOfWeek == 7:
        work = 0
    return work


# 按传入的考勤记录更新模板
def updatedic(labledic, kqdatalist):
    for time in kqdatalist:
        thisdate = time[0:10]  # 获取日期
        thistime = time[-9:]  # 获取时间
        labledic = thistimelist2update(thisdate, thistime, labledic)
    return labledic


# 更新dic的值(判断时间是上班还是下班,且早上只保留最早的,晚上保留最晚的时间)
def thistimelist2update(kdate, vtime, dic):
    kqtime = datetime.strptime(kdate + ' ' + vtime, '%Y-%m-%d %H:%M:%S')
    middletime = datetime.strptime(kdate + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S')
    l = [0, 0]  # 初始化
    if kdate in dic:  # 如果在字典里存在
        l = dic[kdate]
        if kqtime < middletime:  # 上午
            if l[0] == 0:
                l[0] = datetime.strftime(kqtime, '%H:%M:%S')
            else:
                am = datetime.strptime(kdate + ' ' + l[0], '%Y-%m-%d %H:%M:%S')
                if kqtime < am:
                    l[0] = datetime.strftime(kqtime, '%H:%M:%S')
        else:  # 下午
            if l[1] == 0:
                l[1] = datetime.strftime(kqtime, '%H:%M:%S')
            else:
                pm = datetime.strptime(kdate + ' ' + l[1], '%Y-%m-%d %H:%M:%S')
                if kqtime > pm:
                    l[1] = datetime.strftime(kqtime, '%H:%M:%S')
    else:  # 如果在字典里不存在,则添加
        if kqtime < middletime:  # 上午
            l[0] = datetime.strftime(kqtime, '%H:%M:%S')
        else:  # 下午
            l[1] = datetime.strftime(kqtime, '%H:%M:%S')

    dic.update({kdate: l})  # 更新数据
    return dic


# 判断已有模板里哪些是迟到、旷工等情况
def getiskq(newlabledic):
    kqlist = []  # 初始化考勤列表
    for key, value in newlabledic.items():
        if value[0] == 0:
            kqlist.append(key + ' 上班未打卡')
        else:
            kqtime = datetime.strptime(key + ' ' + value[0], '%Y-%m-%d %H:%M:%S')
            sbtime = datetime.strptime(key + ' ' + '9:10:00', '%Y-%m-%d %H:%M:%S')
            yccdtime = datetime.strptime(key + ' ' + '9:30:00', '%Y-%m-%d %H:%M:%S')
            ycxbtime = datetime.strptime(key + ' ' + '18:30:00', '%Y-%m-%d %H:%M:%S')
            if kqtime > yccdtime:
                kqlist.append(key + ' ' + value[0] + ' 上班迟到啦!')
            if sbtime < kqtime <= yccdtime and value[1] != 0:
                xbtime = datetime.strptime(key + ' ' + value[1], '%Y-%m-%d %H:%M:%S')
                if xbtime < ycxbtime:
                    kqlist.append(key + ' ' + value[0] + ' 上班迟到啦!')

        if value[1] == 0:
            kqlist.append(key + ' 下班未打卡')
        else:
            kqtime = datetime.strptime(key + ' ' + value[1], '%Y-%m-%d %H:%M:%S')
            sbtime = datetime.strptime(key + ' ' + '18:00:00', '%Y-%m-%d %H:%M:%S')
            if kqtime < sbtime:
                kqlist.append(key + ' ' + value[1] + ' 下班早退啦!')
    if kqlist == []:
        kqlist = ['恭喜您,全勤!请再接再厉!']

    #把列表转换成字符串并换行显示
    kqstr='\r\n'.join(str(a) for a in kqlist)
    return kqstr
