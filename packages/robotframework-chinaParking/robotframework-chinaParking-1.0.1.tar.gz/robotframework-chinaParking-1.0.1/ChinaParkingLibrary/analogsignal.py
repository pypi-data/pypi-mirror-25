# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta



class AnalogSignal(object):

    A='30010001c000000000'
    B='10aa0021'
    hop_Netid='14d3'
    arrive_signal='191afdedfe24fec402f14532'#驶入信号
    departure_signal='121bffb301bffdfc00000032'#驶离信号
    #chicken_signal='181b03f9fe60fe15056e5b32'
    #move_signal='1b26ff000020ff1d00400432'

    arrive_C='d81000053810'
    departure_C='cd1000053810'
    #chicken_C='cd1000053810'
    #move_C='ab1000049d10'

    erth_type='04'#平行泊位04
    D='01'





    def arrive_xml(self,autotime,seq,sensor_address,gateway_address,gateway_name):#提前时间，传感器地址，网关地址，网关名称
        '''获取模拟地感驶入XML

        参数说明：
        autotime:时间提前或延后量（分钟为单位）
        seq:帧序号（驶入或驶离一次加1）
        sensor_address: 传感器地址
        gateway_address: 网关地址
        gateway_name: 网关名称

        示例：
        |  ${arrivexml}=  | arrive_xml  | 0 | 310094EE |10000538 | ZZZZ   |

        '''
        #换算驶入时间
        now = datetime.now() #获取当前时间
        aMin = timedelta(minutes=int(autotime)) #增加或减少时间（分钟为单位）
        srTime = now+aMin

        sendtime = self.time_to_formate(srTime) #格式化时间

        #换算seq帧
        seq=int(seq)
        while seq > 255:
            seq = seq-255
        seq16="%02X"%(seq)

        #拼接驶入data
        arrive_data=self.A+gateway_address+self.B+sendtime+self.hop_Netid+seq16+self.arrive_C+sensor_address+self.arrive_signal+self.erth_type+self.D

        #拼凑XML
        arrivexml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservice.process.innotek.com" xmlns:xsd="http://webservice.process.innotek.com/xsd">\n'\
        '<soapenv:Header/>\n'\
        '<soapenv:Body>\n'\
        '<web:send>\n'\
        '<!--Optional:-->\n'\
        '<web:nocPacket>\n'\
        '<!--Optional:-->\n'\
        '<xsd:GWName>'+gateway_name+'</xsd:GWName>\n'\
        '<!--Optional:-->\n'\
        '<!--Optional:-->\n'\
        '<xsd:packetType>100</xsd:packetType><xsd:password>123456</xsd:password>\n'\
        '<!--Optional:-->\n'\
        '<xsd:payload>'+arrive_data+'</xsd:payload>\n'\
        '<!--Optional:-->\n'\
        '<xsd:userName>admin</xsd:userName>\n'\
        '</web:nocPacket>\n'\
        '</web:send>\n'\
        '</soapenv:Body>\n'\
        '</soapenv:Envelope>'

        return arrivexml

    def departure_xml(self,autotime,seq,sensor_address,gateway_address,gateway_name):
        '''获取模拟地感驶离XML

        参数说明：
        autotime:时间提前或延后量（分钟为单位）
        seq:帧序号（驶入或驶离一次加1）
        sensor_address: 传感器地址
        gateway_address: 网关地址
        gateway_name: 网关名称

        示例：
        |  ${departurexml}=  | departure_xml  | 0 | 310094EE |10000538 | ZZZZ   |

        '''

         #换算驶离时间
        now = datetime.now() #获取当前时间
        aMin = timedelta(minutes=int(autotime)) #增加或减少时间（分钟为单位）
        slTime = now+aMin

        sendtime = self.time_to_formate(slTime) #格式化时间

        #换算seq帧
        seq=int(seq)
        while seq > 255:
            seq = seq-255
        seq16="%02X"%(seq)

        #拼接驶离data
        departure_data=self.A+gateway_address+self.B+sendtime+self.hop_Netid+seq16+self.departure_C+sensor_address+self.departure_signal+self.erth_type+self.D

        #拼凑XML
        departurexml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservice.process.innotek.com" xmlns:xsd="http://webservice.process.innotek.com/xsd">\n'\
        '<soapenv:Header/>\n'\
        '<soapenv:Body>\n'\
        '<web:send>\n'\
        '<!--Optional:-->\n'\
        '<web:nocPacket>\n'\
        '<!--Optional:-->\n'\
        '<xsd:GWName>'+gateway_name+'</xsd:GWName>\n'\
        '<!--Optional:-->\n'\
        '<!--Optional:-->\n'\
        '<xsd:packetType>100</xsd:packetType><xsd:password>123456</xsd:password>\n'\
        '<!--Optional:-->\n'\
        '<xsd:payload>'+departure_data+'</xsd:payload>\n'\
        '<!--Optional:-->\n'\
        '<xsd:userName>admin</xsd:userName>\n'\
        '</web:nocPacket>\n'\
        '</web:send>\n'\
        '</soapenv:Body>\n'\
        '</soapenv:Envelope>'

        return departurexml




    #把时间格式化成16进制并补位
    def time_to_formate(self,time):
        y = time.strftime('%y')#年
        m = time.strftime('%m')#月
        d = time.strftime('%d')#日
        h = time.strftime('%H')#时
        mm = time.strftime('%M')#分
        s = time.strftime('%S')#秒

        fromate_time = "%02X%02X%02X%02X%02X%02X" % (int(y), int(m), int(d), int(h), int(mm), int(s))
        return fromate_time


#print AnalogSignal().arrive_xml('0','12','310094EE','10000538','ZZZZ')



#print AnalogSignal().departure_xml('0','12','310094EE','10000538','ZZZZ')