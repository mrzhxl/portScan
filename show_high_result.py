#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import redis
import pickle
import os
from config import conf
from jinja2 import Environment, PackageLoader
import sys
from sendmail import sendMail

sys.path.insert(0, '../')

mailto = conf.CONFIG.get('email').get('email_to')

REDIS_HOST = conf.CONFIG.get('redis').get('redis_host')
REDIS_PORT = conf.CONFIG.get('redis').get('redis_port')
REDIS_PASSWORD = conf.CONFIG.get('redis').get('redis_password')

pool = redis.ConnectionPool(host='%s' % REDIS_HOST, password='%s' % REDIS_PASSWORD, port="%d" % REDIS_PORT, db=1,
							decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)


def show_scan_result(result):
	results = {}
	for val in result.values():
		while not val.ready():
			time.sleep(1)

		res = json.loads(r.get('celery-task-meta-' + val.id))  # redis取结果

		# 解析结果
		if res.get('result'):
			for ip in res['result']['scan']:
				ports = []
				for port in res['result']['scan'][ip]['tcp']:
					ports.append(port)
					results[ip] = ports
	# 返回扫描后的全部结果
	return results


if __name__ == '__main__':
	with open(os.getcwd() + '/tmp/' + 'report_high.txt', 'rb') as sfile:
		task_lists = pickle.load(sfile)

	tem = {}
	for project in task_lists:
		for pro_id, tasks_id in project.items():
			results = show_scan_result(tasks_id)
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
		print(report)
		# sendMail(mailto, '端口告警-%s' % times, report)
