#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
import requests
import json
import time
from multiprocessing import Pool as ThreadPool

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import conf


IPLIST_dir = os.getcwd() + '/iplist'

URL = conf.CONFIG.get('cmdb').get('cmdb_host')
username = conf.CONFIG.get('cmdb').get('cmdb_username')
passwd = conf.CONFIG.get('cmdb').get('cmdb_password')

th = 20


class GetCmdbInfo(object):
	def __init__(self, url, username, passwd):
		self.url = url
		self.username = username
		self.passwd = passwd

	# url请求
	def url_get(self,url):
		self.url_res = requests.get(url, auth=(self.username, self.passwd))
		if self.url_res.status_code == 200:
			self.page_text = json.loads(self.url_res.text)
			return self.page_text
		else:
			return 'server err'

	# 下一页
	def ifnext(self, page_text):
		if page_text['next']:
			return page_text['next']
		else:
			return None

	# 获取所有项目
	def get_all_project(self):
		uri = '/projects'
		pros = []
		res = []
		self.page = self.url_get(self.url+uri)	# 第一页全部
		self.results = self.page['results']	# 第一页results
		pros.append(self.results)
		self.next_url = self.ifnext(self.page)	# 返回是否有next
		while self.next_url:
			page = self.url_get(self.next_url)	# 如果有next，继续请求
			results = page['results']

			pros.append(results)
			self.next_url = self.ifnext(page)
		for pro in pros:
			for p in pro:
				res.append(p.get('name'))
		result = set(res)
		return list(result)


	# 获取所有服务器外网ip
	def get_all_ip(self):
		uri = '/instance/?page_size=100'
		ips = []
		res = []
		self.page = self.url_get(self.url + uri)
		self.results = self.page['results']
		ips.append(self.results)
		self.next_url = self.ifnext(self.page)
		while self.next_url:
			page = self.url_get(self.next_url)
			results = page['results']

			ips.append(results)
			self.next_url = self.ifnext(page)

		for ip in ips:
			for i in ip:
				if i.get('instance_status').lower() == 'running':
					if i.get('wip'):
						res.append(i.get('wip'))
		return res

	# 获取项目外网ip
	def get_pro_ip(self, pro):
		'''
		:param pro: 项目
		:return: 项目外网ip
		'''
		uri = '/instance/?project='
		ips = []
		res = []
		self.page = self.url_get(self.url + uri + pro)
		self.results = self.page['results']
		ips.append(self.results)
		self.next_url = self.ifnext(self.page)
		while self.next_url:
			page = self.url_get(self.next_url)
			results = page['results']

			ips.append(results)
			self.next_url = self.ifnext(page)

		for ip in ips:
			for i in ip:
				if i.get('instance_status').lower() == 'running':
					if i.get('wip'):
						res.append(i.get('wip'))
		return res



if __name__ == '__main__':

	# 实例化cmdb类
	ip1 = GetCmdbInfo(URL,username, passwd)

	# 请求所有项目
	pros = ip1.get_all_project()

	# 请求所有服务器ip
	# ips = ip1.get_all_ip()
	# if os.path.exists(IPLIST_dir + '/allip.txt'):
	# 	os.remove(IPLIST_dir + '/allip.txt')
	# for ip in ips:
	# 	with open(IPLIST_dir + '/allip.txt', 'a+') as allip:
	# 		allip.write(ip + '\n')

	def main(pros):
		pro_ips = ip1.get_pro_ip(pros)
		if os.path.exists(IPLIST_dir + '/%s.txt' % pros):
			os.remove(IPLIST_dir + '/%s.txt' % pros)
		for pro_ip in pro_ips:
			with open(IPLIST_dir + '/%s.txt' % pros, 'a+') as proip:
				proip.write(pro_ip + '\n')

	# 多进程请求所有项目ip
	pool = ThreadPool(th)
	pool.map(main, pros)
	pool.close()
	pool.join()