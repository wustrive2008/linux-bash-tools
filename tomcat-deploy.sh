cd /home/lbt/android/apps/tycz-data-layer/project/tycz-data-layer/

echo '将要更新项目tycz-data-layer'
echo -n '是否继续[y/n]:'
logfilename=`date +%Y-%m-%d`
read input
ret=`echo $input | tr '[a-z]' '[A-Z]'`
if [ $ret = "N" ]; then 
   exit 0
fi

echo '更新过程中注意观察日志信息，更新顺序：拉代码->编译/打包->停止tomcat->替换程序->启动tomcat'

gitres=`git pull | wc -l`

echo '正在努力拉取最新代码......'

if [ $gitres -lt 2 ];then
    echo -n '没有拉取到比服务器上更新的代码，是否继续更新![y/n]'
    read input
    ret2=`echo $input | tr '[a-z]' '[A-Z]'`
    if [ $ret2 = "N" ]; then
        exit 0
    fi
fi

mvn clean package -Dmaven.test.skip=true
echo '历史版本:'
git tag -l

echo -n '为新版本打标签,输入标签名称:'
read tag
echo '为新版本输入简单易懂的说明:'
read tagmsg

git tag -a $tag -m $tagmsg

if [ ! $? -eq 0 ]; then
    echo -n '打标签失败，是否继续?[yes/no]'
    read input
    ret3=`echo $input | tr '[a-z]' '[A-Z]'`
    if [ $ret3 != "YES" ]; then
        exit 0
    fi
fi
cd /home/lbt/android/apps/tycz-data-layer/tomcat/node2/
./bin/shutdown.sh
echo '新的代码已重新打包，睡眠3秒后继续！'
sleep 3
rm -r webapps/tycz
cp -rf /home/lbt/android/apps/tycz-data-layer/project/tycz-data-layer/target/tycz webapps/
cp bak/* webapps/tycz-data-layer/WEB-INF/classes/
./bin/startup.sh
echo '正在启动新的程序，注意下面的日志信息，等待启动无误后，按ctrl+C退出即可'
sleep 2
tail -f logs/catalina.out.$logfilename
