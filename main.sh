#!/bin/bash

appdir='/data1/portScan'

lowlogfile='/data1/portScan/logs/lowscan_running.log'
highlogfile='/data1/portScan/logs/highscan_running.log'

allscan(){
    DATE=`date`
    cd $appdir
    echo "----------${DATE}----------" >> $lowlogfile
    echo '获取cmdb信息' >> $lowlogfile
    /root/.pyenv/versions/env3.6/bin/python CmdbGetInfo.py
    sleep 3
    echo '全端口扫描开始....' >> $lowlogfile
    /root/.pyenv/versions/env3.6/bin/python StartScan.py allscan
    if [ $? -eq 0 ];then
        echo '等待获取全端口扫描后的结果.......' >> $lowlogfile
        sleep 600
        echo '正在获取全端口扫描后结果.........' >> $lowlogfile
        /root/.pyenv/versions/env3.6/bin/python show_result.py allport
        if [ $? -eq 0 ];then
            echo '全端口扫描邮件结果已发送........' >> $lowlogfile
        fi
    else
        echo '全端口扫描失败.........'>> $lowlogfile
    fi
}

dangerscan(){
    DATE=`date`
    cd $appdir
    echo "----------${DATE}----------" >> $highlogfile
    echo '获取cmdb信息' >> $highlogfile
    /root/.pyenv/versions/env3.6/bin/python CmdbGetInfo.py
    sleep 3
    echo '高危险扫描开始....' >> $highlogfile
    /root/.pyenv/versions/env3.6/bin/python StartScan.py dangerscan
    if [ $? -eq 0 ];then
        echo '等待获取高危险端口扫描后的结果........' >> $highlogfile
        sleep 300
        echo '正在获取高危险端口扫描后结果.........' >> $highlogfile
        /root/.pyenv/versions/env3.6/bin/python show_result.py dangerport
        if [ $? -eq 0 ];then
            echo '高危险端口扫描邮件结果已发送........' >> $highlogfile
        fi
    else
        echo '高危险端口扫描失败.........'>> $highlogfile
    fi
}

case "$1" in
    danger)
        dangerscan
        ;;
    all)
        allscan
        ;;
    *)
        echo "运行错误，请按照以下参数执行："
        echo "Usage: $0 {danger|all}"
        echo "danger: 高危险端口扫描"
        echo "all: 全端口扫描"
        exit 1
        ;;
esac