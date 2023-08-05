# -*- coding: utf-8 -*-
from packages.baseLib import get_md5_value
from datetime import datetime
from datetime import timedelta

class ParkingLot(object):

    #驶入XML
    def get_in_xml(self,autotime,plateNo,tccid,jrsdm,yptzh,fxlx,pplx,cllx,zxd):#提前量时间，车牌，停车场ID，接入商代码,云平台账号,放行类型,匹配类型,车辆类型,置信度
        '''获取停车场模拟驶入XML

        参数说明：
        autotime:时间提前或延后量（分钟为单位）
        plateNo: 车牌号
        tccid: 停车场ID
        jrsdm:接入商代码
        yptzh: 云平台账号
        fxlx:放行类型
            0.自动开闸; 1.手动开闸; 2.车牌矫正; 3.人工放行
        pplx:匹配类型
            1.完全匹配; 2.手动矫正; 3.人工匹配; 4.模糊匹配
        cllx:车辆类型
            1、普通车辆; 2、包月车辆; 3、特殊车辆; 4、黑名单车辆
        zxd:置信度:0-100

        示例：
        |  ${xml}=  | get_in_xml  | -20 | 浙CSK306 | hzlpdh | keytop    | 0 | 1 | 1 | 99 |

        '''
        ##获取驶入时间
        now = datetime.now() #获取当前时间
        aMin = timedelta(minutes=int(autotime)) #增加或减少时间（分钟为单位）
        srTime = now+aMin
        ##获取驶入流水号
        srsj_lsh = srTime.strftime("%Y%m%d%H%M%S%f")[0:17] #格式化时间，保留17位
        RCLSH = "SRLSH"+get_md5_value(srsj_lsh).upper() #时间用MD5加密后拼接"SRLSH"字符再转换大写

        ##格式化驶入时间
        srsj=srTime.strftime("%Y-%m-%d %H:%M:%S")



        ##拼凑XML
        rkmc="入口名称测试" #入口名称
        cpys="0"#车牌颜色

        ##算出秘钥
        unsign=RCLSH+tccid+rkmc+plateNo+cpys+srsj
        java2same=(yptzh + unsign + jrsdm).encode(encoding='GBK')#这里必须转成GBK，与java里编码一致，不然MD5值会不一样
        sign=get_md5_value(java2same)

        #拼凑xml
        inxml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:fac="http://facade.ws.service.innotek.com/">\n'\
        '<soapenv:Header/>\n'\
        '<soapenv:Body>\n'\
        '<fac:sendApproach>\n'\
        '<arg0>\n'\
        '<![CDATA[\n'\
        '<ROOT>\n'\
        '<YPTZH>{yptzh}</YPTZH>\n'\
        '<CONTENTS>\n'\
        '<CONTENT>\n'\
        '<LSH>{RCLSH}</LSH>\n'\
        '<TCCBH>{tccid}</TCCBH>\n'\
        '<CPH>{plateNo}</CPH>\n'\
        '<CPYS>{cpys}</CPYS>\n'\
        '<SRSJ>{srsj}</SRSJ>\n'\
        '<RKMC>{rkmc}</RKMC>\n'\
        '<FXLX>{fxlx}</FXLX>\n'\
        '<PPLX>{pplx}</PPLX>\n'\
        '<CLLX>{cllx}</CLLX>\n' \
        '<ZXD>{zxd}</ZXD>\n' \
        '</CONTENT>\n'\
        '</CONTENTS>\n'\
        '<SIGN>{sign}</SIGN>\n'\
        '</ROOT>\n'\
        ']]>\n'\
        '</arg0>\n'\
        '</fac:sendApproach>\n'\
        '</soapenv:Body>\n'\
        '</soapenv:Envelope>'.format(yptzh=yptzh,tccid=tccid,RCLSH=RCLSH,plateNo=plateNo,cpys=cpys,srsj=srsj,fxlx=fxlx,pplx=pplx,cllx=cllx,zxd=zxd,rkmc=rkmc,sign=sign)

        return inxml


    ##驶出XML
    def get_out_xml(self,autotime,plateNo,tccid,jrsdm,yptzh,RCLSH,fkje,fkfs,fxlx,pplx,cllx,zxd):#提前量时间，车牌，停车场ID，接入商代码,云平台账号,驶入流水号，付款金额（线下）,付款方式,放行类型,匹配类型,车辆类型,置信度
        '''获取停车场模拟驶离XML

        参数说明：
        autotime:时间提前或延后量（分钟为单位）
        plateNo:车牌号
        tccid:停车场ID
        jrsdm:接入商代码
        yptzh:云平台账号
        RCLSH:驶入时的流水号
        fkje:线下付款金额
        fkfs:付款方式
            1、线上支付宝；2、线上微信；3、现金；4、线下支付宝；5、线下微信；6、市民卡;7、银联; 61、线上一网通
        fxlx:放行类型
            0.自动开闸; 1.手动开闸; 2.车牌矫正; 3.人工放行
        pplx:匹配类型
            1.完全匹配; 2.手动矫正; 3.人工匹配; 4.模糊匹配
        cllx:车辆类型
            1、普通车辆; 2、包月车辆; 3、特殊车辆; 4、黑名单车辆
        zxd:置信度:0-100

        示例：
        | ${xml}= | get_out_xml | -20 | 浙CSK306 | hzlpdh | keytop | RCLSHXXXXXX | 0 | 3 | 0 | 1 | 1 | 99 |

        '''
        ##获取驶出时间
        now = datetime.now() #获取当前时间
        aMin = timedelta(minutes=int(autotime)) #增加或减少时间（分钟为单位）
        ccTime = now+aMin
        ##获取驶出流水号
        slsj_lsh = ccTime.strftime("%Y%m%d%H%M%S%f")[0:17] #格式化时间，保留17位
        CCLSH = "CCLSH"+get_md5_value(slsj_lsh).upper() #时间用MD5加密后拼接"SRLSH"字符再转换大写

        ##格式化驶入时间
        slsj=ccTime.strftime("%Y-%m-%d %H:%M:%S")



        ##拼凑XML
        ckmc="出口名称测试" #入口名称
        cpys="0"#车牌颜色


        ##算出秘钥
        unsign=CCLSH+tccid+ckmc+plateNo+RCLSH+cpys+slsj+fkje
        java2same=(yptzh + unsign + jrsdm).encode(encoding='GBK')#这里必须转成GBK，与java里编码一致，不然MD5值会不一样
        sign=get_md5_value(java2same)

        #拼凑xml
        outxml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:fac="http://facade.ws.service.innotek.com/">\n'\
        '<soapenv:Header/>\n'\
        '<soapenv:Body>\n'\
        '<fac:sendAppearance>\n'\
        '<arg0>\n'\
        '<![CDATA[\n'\
        '<ROOT>\n'\
        '<YPTZH>{yptzh}</YPTZH>\n'\
        '<CONTENTS>\n'\
        '<CONTENT>\n'\
        '<LSH>{CCLSH}</LSH>\n'\
        '<RCLSH>{RCLSH}</RCLSH>\n'\
        '<TCCBH>{tccid}</TCCBH>\n'\
        '<SCCPH>{plateNo}</SCCPH>\n'\
        '<CPYS>{cpys}</CPYS>\n'\
        '<SLSJ>{slsj}</SLSJ>\n'\
        '<FKJE>{fkje}</FKJE>\n'\
        '<FKFS>{fkfs}</FKFS>\n'\
        '<FXLX>{fxlx}</FXLX>\n'\
        '<PPLX>{pplx}</PPLX>\n'\
        '<CLLX>{cllx}</CLLX>\n'\
        '<CKMC>{ckmc}</CKMC>\n'\
        '<ZXD>{zxd}</ZXD>\n'\
        '</CONTENT>\n'\
        '</CONTENTS>\n'\
        '<SIGN>{sign}</SIGN>\n'\
        '</ROOT>\n'\
        ']]>\n'\
        '</arg0>\n'\
        '</fac:sendAppearance>\n'\
        '</soapenv:Body>\n'\
        '</soapenv:Envelope>'.format(yptzh=yptzh,tccid=tccid,CCLSH=CCLSH,RCLSH=RCLSH,plateNo=plateNo,cpys=cpys,slsj=slsj,fkje=fkje,fkfs=fkfs,fxlx=fxlx,pplx=pplx,cllx=cllx,zxd=zxd,ckmc=ckmc,sign=sign)

        return outxml






#print ParkingLot().get_in_xml(-20,'浙TEST02','hzlpdh','比如keytop','0','1','1','100')

#print ParkingLot().get_out_xml(0,'浙TEST02','hzlpdh','keytop','SRLSH8E4A5E9234B287F58C07BC498FADFDCD','0','0','1','1','100')



