#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
#配置信息

#日期
today = datetime.date.today()  
yesterday = today - datetime.timedelta(days = 1)  
tomorrow = today + datetime.timedelta(days = 1)  

#lbt-data-layer
lbt_datalayer_name = 'lbt-data-layer'
lbt_datalayer_log = '../lbt-data-layer-error.log'+'.'+yesterday.strftime('%Y-%m-%d')+'.log'
lbt_datalayer_receiver = ('xxjgxxxx@139.com','137836xxxxxx@163.com')
#lbt_datalayer_receiver = ('18695850831@126.com',)

#lbt-java-web
lbt_weblayer_name = 'lbt-java-web'
lbt_weblayer_log = '../lbt-java-web-error.log'+'.'+yesterday.strftime('%Y-%m-%d')+'.log'
lbt_weblayer_receiver = lbt_datalayer_receiver

#tycz-data-layer
tycz_datalayer_name = 'tycz-data-layer'
tycz_datalayer_log = '../tycz-data-layer-error.log'+'.'+yesterday.strftime('%Y-%m-%d')+'.log'
tycz_datalayer_receiver = lbt_datalayer_receiver


#servers collection
server = {lbt_weblayer_name:(lbt_weblayer_log,lbt_weblayer_receiver),lbt_datalayer_name:(lbt_datalayer_log,lbt_datalayer_receiver),tycz_datalayer_name:(tycz_datalayer_log,tycz_datalayer_receiver)}

#server = {lbt_datalayer_name:(lbt_datalayer_log,lbt_datalayer_receiver)}

#print(weblayerlog)

#print(yesterday.datetime.now().strftime('%Y-%m-%d'))

# for k,v in server.items():
#     print(k+u'服务器Tomcat日志错误信息')
    #print(v[0]+" "+v[1][0]+","+v[1][1])
