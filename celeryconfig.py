#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kombu import Exchange, Queue


REDIS_HOST = ''
REDIS_PORT = 6379
REDIS_PASSWORD = ''

enable_utc = True
timezone = 'Asia/Shanghai'
result_expires = 3600
broker_url = 'amqp://username:password@IP/'		# 因网络原因，尤其是跨国玩两个使用rabbitmq，支持断线重连。redis不支持
result_backend = 'redis://:%s@%s:%d/1' % (REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)
include = ['portScan.tasks']

# 队列
task_queues = (
	Queue("default", Exchange("default"), routing_key="default"),
	Queue("for_task_bjscan", Exchange("for_task_bjscan"), routing_key="for_task_bjscan"),
	Queue("for_task_shscan", Exchange("for_task_shscan"), routing_key="for_task_shscan"),
	Queue("for_task_twscan", Exchange("for_task_twscan"), routing_key="for_task_twscan"),
	Queue("for_task_jpscan", Exchange("for_task_jpscan"), routing_key="for_task_jpscan"),
	Queue("for_task_sgpscan", Exchange("for_task_sgpscan"), routing_key="for_task_sgpscan"),
	Queue("for_task_usscan", Exchange("for_task_usscan"), routing_key="for_task_usscan"),
	Queue("for_task_krscan", Exchange("for_task_krscan"), routing_key="for_task_krscan"),
)
# 路由
task_routes = {
	'portScan.tasks.bj_scan': {"queue": "for_task_bjscan", "routing_key": "for_task_bjscan"},
	'portScan.tasks.sh_scan': {"queue": "for_task_shscan", "routing_key": "for_task_shscan"},
	'portScan.tasks.tw_scan': {"queue": "for_task_twscan", "routing_key": "for_task_twscan"},
	'portScan.tasks.jp_scan': {"queue": "for_task_jpscan", "routing_key": "for_task_jpscan"},
	'portScan.tasks.sgp_scan': {"queue": "for_task_sgpscan", "routing_key": "for_task_sgpscan"},
	'portScan.tasks.us_scan': {"queue": "for_task_usscan", "routing_key": "for_task_usscan"},
	'portScan.tasks.kr_scan': {"queue": "for_task_krscan", "routing_key": "for_task_krscan"},
	'portScan.tasks.send_mail': {"queue": "for_task_bjscan", "routing_key": "for_task_bjscan"}
}
task_default_queue = 'default'  # 设置默认的路由
task_default_exchange = 'default'
task_default_routing_key = 'default'
