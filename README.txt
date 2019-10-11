环境：
python 3.6
masscan

用户：
root


部署脚本:
cd portScan/deploy
sh deploy.sh

安装依赖:
/root/.pyenv/versions/env3.6/bin/pip install -r requirements.txt


启动：
修改/bin目录下portscan.sh中队列名称
source ~/.bashrc
cd bin/
sh portscan.sh start


停止：
cd bin/
sh portscan.sh stop

使用supervisor（服务宕机会自动拉起）
supervisor配置
[program:portscan]
command=/root/.pyenv/versions/env3.6/bin/celery -A portScan  worker -l info -Q 队列名 -c 进程数
directory=程序上级目录
stdout_logfile=日志目录/task_krscan.log
autostart=true
autorestart=true
redirect_stderr=true


文件目录：
portScan
├── CmdbGetInfo.py              # 调用私有cmdb(扫描前需要从cmdb中获取所有项目ip，可以自己造数据，注释掉调用cmdb代码)
├── README.txt                  # 说明
├── WhiteListProcess.py         # 白名单程序
├── __init__.py
├── bin                         # 启动队列脚本目录
│   └── portscan.sh
├── celeryconfig.py             # celery配置文件
├── config                      # 全局配置文件
│   └── conf.py
├── deploy                      # 部署脚本目录
│   ├── Python-3.6.0.tar.xz
│   ├── deploy.sh               # 部署脚本
│   ├── masscan                 # 扫描工具
│   └── pyenv-installer         # pyenv虚拟环境安装脚本
├── highscan.py                 # 高危端口扫描
├── iplist                      # 项目ip列表，每个项目一个文件
│   ├── 项目名.txt
├── logs                        # 日志目录
├── lowscan.py                  # 全部端口扫描
├── main.sh
├── portlist                    # 端口目录，每个项目一个文件，danger_ports.txt高危端口列表，all_ports.txt为全部扫描的端口列表
│   ├── all_ports.txt
│   └── danger_ports.txt
├── requirements.txt            # 依赖包
├── sendmail.py                 # 发送邮件脚本
├── show_high_result.py         # 获取高危端口扫描后的数据
├── show_low_result.py          # 获取全部端口扫描后的数据
├── tasks.py                    # 任务
├── templates                   # 模板
│   └── report.html
└── tmp                         # 序列化数据
    └── report.txt

