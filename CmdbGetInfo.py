#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
import requests
import json
import yaml


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import conf


IPLIST_dir = os.getcwd() + '/iplist'
PORTLIST_dir = os.getcwd() + '/portlist'

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

	# 获取所有服务器信息
	def get_all_info(self, pro):
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

		for infos in ips:
			for info in infos:
				if info.get('instance_status').lower() == 'running':
					if info.get('wip'):
						res.append(info)
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

	# 获取项目服务类型
	def application(self,):
		uri = '/instance'
		apps = []
		dic = {}
		self.page = self.url_get(self.url + uri)
		self.results = self.page['results']
		apps.append(self.results)
		self.next_url = self.ifnext(self.page)
		while self.next_url:
			page = self.url_get(self.next_url)
			results = page['results']

			apps.append(results)
			self.next_url = self.ifnext(page)

		for instance in apps:
			for ins in instance:
				if ins.get('instance_status').lower() == 'running':
					if ins.get('wip'):
						features = ins.get('application').replace(ins.get('project') + '-', '')
						if ins.get('project') in dic.keys():
							dic[ins.get('project')].update({features: '[]'})
						else:
							dic[ins.get('project')] = {features: '[]'}
		#print(dic)
		return dic



# yaml转字典
class get_yaml:
	def __init__(self, file):
		self.filename = file
		self.yaml_data = self.__check_file()
	def __check_file(self):
		path = os.path.dirname(os.path.abspath(__file__))
		file = PORTLIST_dir + self.filename
		if os.path.exists(file):
			with open(file, encoding="utf-8") as yaml_obj:
				yaml_data = yaml_obj.read()
			return yaml_data
		else:
			print('没有yaml文件')
			exit(1)
	def get_yaml_data(self):
		data = yaml.load(self.yaml_data,Loader=yaml.FullLoader)
		return data


if __name__ == '__main__':

	# 实例化cmdb类
	ip1 = GetCmdbInfo(URL,username, passwd)

	# 请求所有项目
	pros = ip1.get_all_project()

	# 读取本地yml
	obj = get_yaml('/all_project_port.yml')
	os.rename(PORTLIST_dir + '/all_project_port.yml', PORTLIST_dir + '/project_port.yml')
	data = obj.get_yaml_data()


	def main():
		app = ip1.application()

		for i in app:
			for n in app[i]:
				if n not in data[i]:
					data[i][n] = []

		with open(PORTLIST_dir + '/all_project_port.yml', 'a+', encoding='utf-8') as f:
			for project in data.keys():
				f.write(project + ':\n')
				for features, value in data[project].items():
					f.write('  ' + features + ':' + ' ' + json.dumps(value) + '\n')



	# 多进程请求所有项目ip
	# pool = ThreadPool(th)
	# if os.path.exists(PORTLIST_dir + '/all_project_port.yml'):
	# 		os.remove(PORTLIST_dir + '/all_project_port.yml')
	# pool.map(main, pros)
	# pool.close()
	# pool.join()



	main()

