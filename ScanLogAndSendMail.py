#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from os.path import getsize
import os
from sys import exit
import re
import pymssql
import datetime
import sys
sys.path.append("../conf")  #最好改为绝对路径
import logmanageconf

#定义主机 帐号 密码 收件人 邮件主题
smtpserver = 'smtp.163.com'
sender = 'xxxxxx@163.com'
password = 'xxxxx'
#receiver = ('18695850831@126.com','15038056331@139.com')
#subject = u'测试web服务器Tomcat日志错误信息'
#From = 'log-server<logServer@shsz.com>'
From = 'sendexception@163.com'
To = 'shsz<yx@shsz.com>'

##定义数据库信息
dbaddress='192.168.32.102'
dbuser='username'
dbpassword='password'
dbname='dbname'

#定义tomcat日志文件位置
#tomcat_log = 'D:\\tyczError.txt'

#日期正则
pattern = re.compile(r'^\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2}$',re.I)

#获取今天和昨天的日期
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)

#发送邮件函数
def send_mail(error,receiver,subject):

    #定义邮件的头部信息
    msg = MIMEText(error)
    msg['Content-Type'] = 'Text/HTML';
    msg['From'] = From
    msg['To'] = To
    msg['Subject'] = Header(subject+'\n','utf-8')

    #连接SMTP服务器，然后发送信息
    smtp = SMTP(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.close()


try:
    conn=pymssql.connect(host=dbaddress,user=dbuser,password=dbpassword,database=dbname)
except:
    print ("Could not connect to mssql server.")
    exit(0)

for servername,logandrece in logmanageconf.server.items():
    try:
        if os.path.isfile(logandrece[0]):
            #以二进制方式读取，防止编码问题导致错误
            data = open(logandrece[0],'rb')
            logfilename = logandrece[0]
        else:
            data = open(logandrece[0][:-15],'rb')
            logfilename = logandrece[0][:-15]
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(logfilename)).strftime("%Y-%m-%d")
            if mtime != yesterday.strftime("%Y-%m-%d"):
                continue
    except:
        print("Could not open log file.")
        #关闭数据库的连接
        conn.close()

    #创建游标对象，相当于ADO的记录集
    cou=conn.cursor()
    #Email内容
    mailContent=data.read().decode()

    if len(mailContent) < 20:
        continue

    #设置文件指针位置，跳过文件头内容
    data.seek(3)
    for line in data:
        errorLine = line.decode()
        #日志分割
        logtime = errorLine[0:19]
        #过滤堆栈
        match = pattern.match(logtime)
        if not match:
            continue
        level = (errorLine.split(' - '))[1][1:6]
        errorinfo = (errorLine.split(' - '))[1][8:]
        errorinfo = errorinfo.replace("'","''")
        inserttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql="Insert into errorlog(appName,logTime,logLevel,logInfo,insertTime) values('%s','%s','%s','%s','%s')" %(servername,logtime,level,errorinfo,inserttime)
        #插入一条记录
        cou.execute(sql)
        #只有执行了下面的命令，上面的操作才能生效
        conn.commit()
    #发送Email
    send_mail(mailContent,logandrece[1],servername + u'服务器Tomcat错误日志.' + yesterday.strftime('%Y-%m-%d'))
    #关闭日志文件
    data.close()
#关闭数据库的连接
conn.close()
