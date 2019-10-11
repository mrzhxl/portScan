#!/bin/bash

appdir='/data1/portScan'

lowlogfile='/data1/portScan/logs/lowscan_running.log'
highlowfile='/data1/portScan/logs/highscan_running.log'

lowscan(){
    DATE=`date`
    cd $appdir
    echo "----------${DATE}----------" >> $lowlogfile
    echo '获取cmdb信息' >> $lowlogfile
    /root/.pyenv/versions/env3.6/bin/python CmdbGetInfo.py
    sleep 3
    echo '全端口扫描开始....' >> $lowlogfile
    /root/.pyenv/versions/env3.6/bin/python lowscan.py
    if [ $? -eq 0 ];then
        echo '等待获取全端口扫描后的结果.......' >> $lowlogfile
        sleep 600
        echo '正在获取全端口扫描后结果.........' >> $lowlogfile
        /root/.pyenv/versions/env3.6/bin/python show_low_result.py
        if [ $? -eq 0 ];then
            echo '全端口扫描邮件结果已发送........' >> $lowlogfile
        fi
    else
        echo '全端口扫描失败.........'>> $lowlogfile
    fi
}

highscan(){
    DATE=`date`
    cd $appdir
    echo "----------${DATE}----------" >> $highlowfile
    echo '获取cmdb信息' >> $highlowfile
    /root/.pyenv/versions/env3.6/bin/python CmdbGetInfo.py
    sleep 3
    echo '高危险扫描开始....' >> $highlowfile
    /root/.pyenv/versions/env3.6/bin/python highscan.py
    if [ $? -eq 0 ];then
        echo '等待获取高危险端口扫描后的结果........' >> $highlowfile
        sleep 300
        echo '正在获取高危险端口扫描后结果.........' >> $highlowfile
        /root/.pyenv/versions/env3.6/bin/python show_high_result.py
        if [ $? -eq 0 ];then
            echo '高危险端口扫描邮件结果已发送........' >> $highlowfile
        fi
    else
        echo '高危险端口扫描失败.........'>> $highlowfile
    fi
}

case "$1" in
    high)
        highscan
        ;;
    low)
        lowscan
        ;;
    *)
        echo "运行错误，请按照以下参数执行："
        echo "Usage: $0 {high|low}"
        echo "highscan: 高危险端口扫描"
        echo "lowscan: 全端口扫描"
        exit 1
        ;;
esac