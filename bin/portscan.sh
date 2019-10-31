#!/usr/bin/env bash


pid='/var/run/portscan.pid'

server_start(){
    if [ -f $pid ];then
        echo '服务运行中'
    fi
    cd ../../
    /root/.pyenv/versions/env3.6/bin/celery -A portScan  worker -l info -Q for_task_bjscan -c 20 &> /data1/portScan/logs/task_bjscan.log &
    if [ "$?" -eq 0 ];then
        touch $pid
        echo '服务已启动'
    else
        echo '系统错误'
    fi
}

server_stop(){
    if [ -f $pid ];then
        ps -ef | grep -v grep | grep celery | awk '{print $2}'| xargs kill -9
        rm -f $pid
        echo '服务已停止'
    else
        echo "服务未启动"
    fi
}


case "$1" in
    start)
        server_start
        ;;
    stop)
        server_stop
        ;;
    *)
        echo "运行错误，请按照以下参数执行："
        echo "Usage: $0 {start|stop}"
        echo "start: 启动服务"
        echo "stop: 停止服务"
        exit 1
        ;;
esac