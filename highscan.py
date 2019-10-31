#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import redis
from config import conf
import pickle

sys.path.insert(0, '../')
obj = __import__('highscan')

from portScan.tasks import *
from WhiteListProcess import checkPort,DangerPort
from CmdbGetInfo import GetCmdbInfo,get_yaml


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

if __name__ == '__main__':
    starttime = time.time()

    high = High_scan()

    # 调用cmdb获取项目，可以自己造pros列表
    getcmdb = GetCmdbInfo(URL,username, passwd)
    Yaml = get_yaml('/all_project_port.yml')
    data = Yaml.get_yaml_data()
    pros = getcmdb.get_all_project()
    # pros = ['GJDJ', 'PT']

    '''
    pros = ['pro1', 'pro2', 'pro3']
    '''
    task_lists = []
    for pro in pros:
        server_info = getcmdb.get_all_info(pro)
        dic = {}
        for ins in server_info:
            features = ins['application'].replace(ins['project'] + '-', '')
            if features in dic.keys():
                dic[features].append(ins['wip'])
            else:
                dic[features] = [ins['wip']]
        try:
            if pro.startswith('KR'):
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'kr')

            elif pro.startswith('JP'):
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'jp')

            elif pro.startswith('SGP'):
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'sgp')

            elif pro.startswith('TW'):
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'tw')

            elif pro.startswith('US'):
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'us')
            else:
                task_id = high.start_scan(dic, data[pro], 'danger_ports.txt', 'bj')
            task_lists.append({pro: task_id})


        except FileNotFoundError as e:
            continue
        except KeyError as e:
            # print('该项目下没有服务器',e)
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