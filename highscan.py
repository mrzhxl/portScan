#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import redis
import json
from jinja2 import Environment, PackageLoader
from config import conf
from sendmail import sendMail
import pickle

sys.path.insert(0, '../')
obj = __import__('highscan')

from portScan.tasks import *
from WhiteListProcess import checkPort
from CmdbGetInfo import GetCmdbInfo


URL = conf.CONFIG.get('cmdb').get('cmdb_host')
username = conf.CONFIG.get('cmdb').get('cmdb_username')
passwd = conf.CONFIG.get('cmdb').get('cmdb_password')
mailto = conf.CONFIG.get('email').get('email_to')

REDIS_HOST = conf.CONFIG.get('redis').get('redis_host')
REDIS_PORT = conf.CONFIG.get('redis').get('redis_port')
REDIS_PASSWORD = conf.CONFIG.get('redis').get('redis_password')


pool = redis.ConnectionPool(host='%s' % REDIS_HOST, password='%s' % REDIS_PASSWORD, port="%d" % REDIS_PORT, db=1, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

class High_scan(object):

    def start_scan(self, ProPortFile, AllPortFile, ProIPfile, region):
        """
        :param ProPortFile: 项目端口文件（白名单）
        :param AllPortFile: 检查的端口文件
        :param ProIPfile: 扫描的服务器列表
        :param region: 地区（分配work）
        :return: 扫描结果（字典）
        """
        PORTS = checkPort(ProPortFile, AllPortFile)
        result = {}
        with open(os.getcwd() + '/iplist/' + ProIPfile, 'r') as ipfile:

            ipfile = ipfile.readlines()

        for ip in ipfile:
            if ip:
                # res = bj_scan.delay(ip, PORTS)
                func = getattr(obj, '%s_scan' % region)     # 根据地区反射
                res = func.delay(ip, PORTS)

                result[ip] = res
        return result




if __name__ == '__main__':
    starttime = time.time()

    high = High_scan()

    # 调用cmdb获取项目，可以自己造pros列表
    getcmdb = GetCmdbInfo(URL,username, passwd)
    pros = getcmdb.get_all_project()

    '''
    pros = ['pro1', 'pro2', 'pro3']
    '''

    task_lists = []
    for pro in pros:
        try:
            if pro.startswith('KR'):
                kr_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'kr')
                task_lists.append({pro: kr_task_id})

            elif pro.startswith('JP'):
                jp_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'jp')
                task_lists.append({pro: jp_task_id})

            elif pro.startswith('SGP'):
                sgp_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'sgp')
                task_lists.append({pro: sgp_task_id})

            elif pro.startswith('TW'):
                tw_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'tw')
                task_lists.append({pro: tw_task_id})

            elif pro.startswith('US'):
                us_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'us')
                task_lists.append({pro: us_task_id})

            else:
                bj_task_id = high.start_scan('%s_ports.txt' % pro, 'danger_ports.txt', '%s.txt' % pro, 'bj')
                task_lists.append({pro: bj_task_id})

        except FileNotFoundError as e:
            continue

    s = pickle.dumps(task_lists)
    with open(os.getcwd() + '/tmp/' + 'report_high.txt', 'wb') as sfile:
        sfile.write(s)



    """
    返回示例
    tem = {
        '项目名': {
            '项目名': '项目名',
            'ip_port': {
                'IP': ['22'],
                'IP': ['80'],
            }
        },
        '项目名': {
            '项目名': '项目名',
            'ip_port': {
                'IP': ['22','443','8080'],
                'IP': ['80'],
            }
        }
    }
    """




