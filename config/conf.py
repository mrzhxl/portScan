#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CONFIG = {
	# 任务结果存放在redis中，此配置是从redis中取出结果
	'redis': {
		'redis_host': '',
		'redis_port': 6379,
		'redis_password': '',
	},
	# 发送邮件
	'email': {
		'email_host': '',
		'email_username': '',
		'email_password': '',
		'email_to': '',
	},
	# 根据实际情况填写，如果没有cmdb，扫描的IP和项目需要自己手动生成
	'cmdb': {
		'cmdb_host': '',
		'cmdb_username': '',
		'cmdb_password': '',
	},
	# 微信报警
	'weixin': {
		'Alertuserlist' : [],
		'WeixinAlertUrl' : ''
	}
}
