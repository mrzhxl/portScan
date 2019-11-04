#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import redis
import pickle
import os
from config import conf
from jinja2 import Environment, PackageLoader
import sys
from sendmail import sendMail, weixin_alert
from ScanTool import Scan

sys.path.insert(0, '../')

mailto = conf.CONFIG.get('email').get('email_to')

REDIS_HOST = conf.CONFIG.get('redis').get('redis_host')
REDIS_PORT = conf.CONFIG.get('redis').get('redis_port')
REDIS_PASSWORD = conf.CONFIG.get('redis').get('redis_password')

Alertuserlist = conf.CONFIG.get('weixin').get('Alertuserlist')

pool = redis.ConnectionPool(host='%s' % REDIS_HOST, password='%s' % REDIS_PASSWORD, port="%d" % REDIS_PORT, db=1,
							decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)


def display_result(clobj, reportFile):
	scan = clobj()
	with open(os.getcwd() + '/tmp/' + '%s' % reportFile, 'rb') as sfile:
		task_lists = pickle.load(sfile)

	tem = {}
	for project in task_lists:
		for pro_id, tasks_id in project.items():
			results = scan.show_scan_result(tasks_id)
			tem[pro_id] = {pro_id: pro_id, 'ip_port': results}

	for project in list(tem.keys()):

		# 剔除扫描结果中为空的项目
		if not tem[project]['ip_port']:
			tem.pop(project)

	if tem:
		# 使用jinja2模板
		env = Environment(loader=PackageLoader('portScan', 'templates'))
		template = env.get_template('report.html')
		try:
			report = template.render(tem=tem)
		except Exception as e:
			print(e)

		times = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		# print(report)

		# 发送邮件
		sendMail(mailto, '端口告警-%s' % times, report)

		# 微信
		data = []
		for project in tem:
			for ip, port in tem[project]['ip_port'].items():
				data1 = ip + '%s' % port
				data.append(data1)

			message = '端口告警：'+ project + '\t' + '%s' % data
			weixin_alert(Alertuserlist, message)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'dangerport':
			display_result(Scan, 'report_high.txt')
		elif sys.argv[1] == 'allport':
			display_result(Scan, 'report_low.txt')
	else:
		print('Usage: %s {dangerport|allport}' % sys.argv[0])
