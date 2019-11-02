#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import redis
import json
from config import conf


sys.path.insert(0, '../')
obj = __import__('ScanTool')

from portScan.tasks import *
from WhiteListProcess import checkPort


REDIS_HOST = conf.CONFIG.get('redis').get('redis_host')
REDIS_PORT = conf.CONFIG.get('redis').get('redis_port')
REDIS_PASSWORD = conf.CONFIG.get('redis').get('redis_password')


pool = redis.ConnectionPool(host='%s' % REDIS_HOST, password='%s' % REDIS_PASSWORD, port="%d" % REDIS_PORT, db=1, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

class Scan(object):

    def start_scan(self, app_ips, app_ports, AllPortFile, region):
        """
        :param app_ips: 项目ip
        :param app_ports: 项目端口（白名单）
        :param AllPortFile: 扫描的服务器列表
        :param region: 地区（分配work）
        :return: 扫描结果（字典）
        """
        result = {}
        for app, app_port in app_ports.items():
            if app in app_ips:
                PORTS = checkPort(app_port, AllPortFile)
                for ip in app_ips[app]:
                    func = getattr(obj, '%s_scan' % region)  # 根据地区反射
                    res = func.delay(ip, PORTS)
                    result[ip] = res

            else:
                print('服务名字对不上：',app)
        return result

    def show_scan_result(self, result):
        """
        :param result:
        :return:
        {
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
    pass
