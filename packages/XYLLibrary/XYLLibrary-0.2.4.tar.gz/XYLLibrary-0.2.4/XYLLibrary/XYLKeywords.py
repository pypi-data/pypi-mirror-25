#-*- coding:utf-8 -*-
__version__='0.1'
from robot.api import logger
import re
import datetime,time
import random
import json
import types
import os
import hashlib
import base64
import requests


class XYLKeywords(object):

    def split_data(self,value,fh=" "):
        '''
        切分数据,返回数组,例如:
        str=3.14.15

        |split data|str|

        return ['3','14','15']
        '''
        if not fh:
            fh=" ";
        return value.split(fh)

    def re_search(self,str,Ls,Rs):
        '''
        通过正则查询结果

        str 被切的数据
        Ls  左边界
        Rs  右边界
        如有多个只取第一个
        Examples:

        | re search | abcd | a | d                                           | # 返回结果是bc

        '''
        m=re.search( Ls+'(.*?)'+Rs,str)
        if m is not None:
            return m.group(1)
            logger.debug('return'+m.group(1))
        else:
            logger.info(str)

    def re_search_all(self,str,Ls,Rs):
        '''
        通过正则查询结果

        str 被切的数据
        Ls  左边界
        Rs  右边界
        返回list
        Examples:

        | re search all | A111B  A222B | A | B                                          | # 返回结果是['111','222']

        '''

        pat=re.compile(Ls+'(.*?)'+Rs)
        m=re.findall(pat,str)
        if m is not None:
            return m
        else:
            logger.info('re_search_all >> None')


    def Get_Time_Modified(self,addnumber='0'):
        '''
        获得当前日期. 可以通过参数加减日期

        :param addnumber: 加减天数, 默认是今天

        :return: str

        '''
        d1 = datetime.date.today()
        d2=d1+datetime.timedelta(int(addnumber))
        return d2

    def Get_Timestamp(self):
        '''
        获得时间戳

        :return: str , 保证数字唯一
        如: 1464921407
        '''
        res=time.time()
        return str(int(res))

    def Random_Num(self,start=1,stop=10000,times=1):
        '''
        随机产生一个随机数

        :param start 随机数最小值 默认是1

        :param stop  随机数最大值 默认是10000

        :param times 倍数,用于凑整随机, 默认是1

        :return: str
        如:

        Random Num | start=1 | stop=10 | times=100  返回 100 ~ 1000 的随机 返回结果为 100 或 200 等
        '''
        num=random.randint(int(start),int(stop))
        num=num*times
        logger.debug('生成随机数:'+str(num))
        return num

    def Random_Choice(self,sequence):
        '''
        随机选择有序类型(如数组)中的某一个值

        :param sequence 有序类型.
        :return 根据你传的参数决定类型
        如:

        Random Choice | ['a','b','c']  返回 a,b,c中的随机一个

        Random Choice | hello    返回h,e,l,l,o 中的随机一个
        '''
        res=random.choice(sequence)
        return res

    def json_Dumps(self,obj):
        '''
        :param obj: 字典或者str类型dumps后会变成json格式. 注意其他类型的会报错
        :return: json
        '''
        if type(obj) is types.UnicodeType:
            obj=obj.encode('utf-8')
        logger.debug(type(obj))
        logger.debug(obj)
        if isinstance(obj,str):
            d=json.JSONDecoder().decode(obj)
            data=json.dumps(d)
        elif isinstance(obj,dict) or isinstance(obj,list):
            data=json.dumps(obj)

        else:
            logger.error("typeError: can't dumps "+str(type(obj)) +" . must <str> or <dict> ")

        return data

    def FormData_to_Dict(self,text):
        '''
        text格式参考 casenumber=&searoute=null&isExsitAdjunct=&currentDate=2016-02-05
        :param text: str
        :return:dict
        '''
        adict={}
        for a in text.split('&'):
            (key,value)= a.split('=')
            adict[key]=value
        return adict

    def Jsonstr_to_Dict(self,jsonStr):
        '''
        text格式参考json 如 {"a":1,"b":2,"3":"c","4":["k","k1"]}
        '''
        d=json.JSONDecoder().decode(jsonStr)
        return d

    def steplog(self,msg):
        '''
        写入格式如:
        2015-12-14   XXXXX
        '''
        #print type(msg)
        #print msg
        #RF传入的是UnicodeType,先转成str
        if type(msg) is types.UnicodeType:
            msg=msg.encode('utf-8')
        path=os.getcwd()
        projectpath=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        logpath=projectpath+os.sep+"steplog"
        if not os.path.exists(logpath):
            logpath=os.mkdir(projectpath+os.sep+"steplog")
        print logpath
        try:
            with open(logpath+os.sep+time.strftime("%Y-%m-%d")+'log.txt','a') as logs:
                logs.write(time.strftime("%H:%M:%S") + "    "+msg+"\n")
        except Exception, e:
            raise e


    def md5(self,str):
        """
        :return: md5 str
        """
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def img_to_base64(self,img_path):
        with open(img_path,'rb') as f:
            f_base64=base64.b64encode(f.read())
        return f_base64

    def get_sms(self, mobile=None):
        """
        :return: 只返回最新的一个验证码
        """

        with requests.Session() as s:
            data = {"userName":"admin", "password": "9eb4a77d869684de82350b750557c714"}
            login = s.post("http://192.168.100.153:8080/sms-back-service-rs/loginUser.htm", data=data)
            #print login.text

            startDate = self.Get_Time_Modified(-30)
            endDate = self.Get_Time_Modified()
            headers = {"Content-Type":"application/json;charset=UTF-8"}
            data2 = {"pageSize":10,"pageIndex":1,"mobile":mobile,"startDate":str(startDate),"endDate":str(endDate),"clientId":"1,2,3,4,5,6,7,8,9","smsProviderId":"1,2,3","scene":"1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40","reptStatus":"1,2,3,99,4,5","clientReptStatus":"0,1,2,3"}
            sms_search = s.post("http://192.168.100.153:8080/sms-back-service-rs/sms/search/smsSendList.htm",headers=headers,data=json.dumps(data2))
            smsJson = sms_search.json()
            if smsJson["data"]["list"] :
                sms_content = smsJson["data"]["list"][0]["smsContent"]
                #sms_code = re.sub("\D", "", sms_content)
                sms_codes = re.findall("\d+", sms_content)
                sms_code = ""
                for s in sms_codes:
                    if len(s) > 2 and len(s) < 8:
                        sms_code = s
                return sms_code
            else:
                return "no sms code"




'''

def conn(hostStr,userStr,passwdStr,dbStr,portInt=3306):
    try:
        conn=MySQLdb.connect(host=hostStr,user=userStr,passwd=passwdStr,db=dbStr,port=portInt)
        cur=conn.cursor()
        return cur

    except MySQLdb.Error,e:
        print "Error: %d : %s" % (e.args[0],e.args[1])
'''


if __name__ == '__main__':

    test=XYLKeywords().img_to_base64("D:\\base64test.jpg")
    print test



