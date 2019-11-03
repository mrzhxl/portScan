# 使用说明

该程序是python+celery+masscan的端口扫描工具

celery的异步功能并结合masscan快速扫描，及时知晓你线上服务器开放了那些非标端口。

masscan地址：https://github.com/robertdavidgraham/masscan

celery地址：https://github.com/celery/celery/wiki

该工具分为：任务端（生产端），和执行任务端（消费端）

## 运行环境：

Centos 7及以上版本

python 3.6

masscan

## 环境部署脚本：

```shell
cd portScan/deploy
sh deploy.sh
```

## 安装依赖

```shell
/root/.pyenv/versions/env3.6/bin/pip install -r requirements.txt
```

## 消费端说明

### 修改消费端配置

```shell
broker_url = 'amqp://guest:guest@localhost:5672//'  # rabbitmq或redis，建议使用rabbitmq，网络不佳的情况下可以断线重连
result_backend = 'redis://localhost:6379/1'         # rabbitmq或redis
include = ['portScan.tasks']

# 队列，可根据现有环境自行修改
task_queues = ()
# 路由，可根据队列名自行修改
task_routes = {}
```

### 启动消费端

```shell
# 修改/bin目录下portscan.sh中队列名称
source ~/.bashrc
cd bin/
sh portscan.sh start
```

### 停止消费端

```shell
cd bin/
sh portscan.sh stop
```

### 使用supervisor启动消费端（服务宕机会自动拉起）

```shell
# supervisor配置
[program:portscan]
command=/root/.pyenv/versions/env3.6/bin/celery -A portScan  worker -l info -Q 队列名 -c 进程数
directory=程序上级目录
stdout_logfile=日志目录/task_krscan.log
autostart=true
autorestart=true
redirect_stderr=true

# supervisor启动消费端
supervisord
```

## 生产端说明

### 修改配置

```shell
config/conf.py  # 根据实际情况填入
celeryconfig.py # 和消费端一致
```

### 扫描

```shell
python StartScan.py {dangerscan|allscan} 
# dangerscan: 危险端口扫描  (扫描portlist/danger_ports.txt文件中的端口)
# allscan: 全端口扫描     (扫描portlist/all_ports.txt文件中的端口)
```

### 获取扫描后的结果

```shell
python show_result.py {dangerport|allport}
# dangerport： 获取危险端口扫描后的结果
# allport： 获取全端口扫描后的结果

说明：需要扫描任务全部执行完毕后才能获取的结果，结果可以发邮件、微信
```

###  扫描+获取结果

```shell
# 使用shell脚本（根据任务执行的速度自行修改等待时间）
sh main.sh {danger|all}

# danger: 扫描危险端口等待5分钟后获取结果
# all：扫描全部端口等待10分钟后获取结果
```

## 白名单功能

如果不需要扫描某应用的端口（正常业务端口），只需要将端口加入到portlist/all_project_port.yml中



## 特殊说明

如果在使用环境中没有CMDB请阅读ScanTool.py文件代码，自行更改程序，来获取IP和项目



有使用问题和建议，请提交issues
