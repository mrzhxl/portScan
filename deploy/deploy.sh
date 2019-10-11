#!/bin/bash


# 配置环境
yum install readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel  bzip2-devel bzip2-libs git gcc gcc-c++ supervisor libpcap-devel python-virtualenv -y
bash pyenv-installer

echo 'eval "$(/root/.pyenv/bin/pyenv init -)"' >> ~/.bashrc
echo 'eval "$(/root/.pyenv/bin/pyenv virtualenv-init -)"' >> ~/.bashrc

mkdir /root/.pyenv/cache/
cp Python-3.6.0.tar.xz /root/.pyenv/cache/


# 安装masscan
mv masscan ../
cd ../
pwd=`pwd`
cd masscan && make



centos6=`cat /etc/redhat-release | grep 6`
if [ -n $centos6 ];then
    git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
fi

# 安装环境
/root/.pyenv/bin/pyenv install 3.6.0
/root/.pyenv/bin/pyenv virtualenv 3.6.0 env3.6

# 修改环境变量
echo "export PATH=/root/.pyenv/versions/env3.6/bin:/root/.pyenv/bin:${pwd}/masscan/bin:$PATH" >> ~/.bashrc