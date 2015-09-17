#########################################################################
# File Name: tomcat-jk.sh
# Author: wustrive
# mail: wustrive2008@gmail.com
# Created Time: Thu 02 Jul 2015 03:28:56 PM CST
#########################################################################
#!/bin/bash

#获取需要监控的tomcat进程PID
#tycz-data-layer
tyczdatalayerPID=$(ps -ef | grep '/tycz-data-layer/' |grep "Bootstrap start"| grep -v 'grep' | awk '{print $2}')
if [ ! "$tyczdatalayerPID" ];then
	tyczdatalayerPID=-1
fi

#lbt-java-web
lbtjavawebPID=$(ps -ef | grep '/web-layer/' |grep "Bootstrap start"| grep -v 'grep' | awk '{print $2}')
if [ ! "$lbtjavawebPID" ];then
    lbtjavawebPID=-1
fi

#lbt-data-layer
lbtdatalayerPID=$(ps -ef | grep '/data-layer/' |grep "Bootstrap start"| grep -v 'grep' | awk '{print $2}')
if [ ! "$lbtdatalayerPID" ];then
    lbtdatalayerPID=-1
fi
#tomcat启动位置
tyczdatalayerStartTomcat=/tomcat/bin/startup.sh
lbtjavawebStartTomcat=/tomcat/node1/bin/startup.sh
lbtdatalayerStartTomcat=/tomcat/node1/bin/startup.sh

#日志记录位置
GetPageInfo=/log/TomcatMonitor.info
TomcatMonitorLog=/log/TomcatMonitor.log

#监控URL
tyczdatalayertestURL='http://127.0.0.1:8080/tycz/rest/cstoryType/findByType.do'
lbtjavawebtestURL='http://www.lebeitong.com'
lbtdatalayertestURL='http://127.0.0.1:8081/lbt/rest/order/groupOrder.do'
monitor()
{
    echo "[info]开始监控tomcat $1 [$(date +'%F %H:%M:%S')]"
    if [ $2 -ne -1 ];then
        echo "[info]当前tomcat进程ID为:$2,继续检测页面..."
        TomcatServiceCode=$(curl -I -m 10 -o $GetPageInfo -s -w %{http_code} $3)
        if [ "$TomcatServiceCode" -eq 405 ] || [ "$TomcatServiceCode" -eq 200 ];then
            echo "[info]页面返回码为$TomcatServiceCode,tomcat运行正常，测试页面访问正常......"
        else
            echo "[error]tomcat页面访问出错......,状态码为:$TomcatServiceCode"
            echo "[error]开始重启tomcat进程"
            kill -9 $2
            sleep 3
            $4
        fi
    else
        echo "[error]tomcat 进程不存在！tomcat开始自动启动..."
        echo "[info]$4,请稍等......"
        $4
    fi
    echo "[info]本次扫描 $1 完成 ........."

}
monitor "tycz-data-layer" $tyczdatalayerPID  $tyczdatalayertestURL  $tyczdatalayerStartTomcat >>$TomcatMonitorLog
monitor "lbt-java-web" $lbtjavawebPID  $lbtjavawebtestURL  $lbtjavawebStartTomcat >>$TomcatMonitorLog
monitor "lbt-data-layer" $lbtdatalayerPID  $lbtdatalayertestURL  $lbtdatalayerStartTomcat >>$TomcatMonitorLog
