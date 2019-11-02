#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from config import conf
import pickle


sys.path.insert(0, '../')

from portScan.tasks import *
from CmdbGetInfo import GetCmdbInfo,get_yaml
from ScanTool import Scan


URL = conf.CONFIG.get('cmdb').get('cmdb_host')
username = conf.CONFIG.get('cmdb').get('cmdb_username')
passwd = conf.CONFIG.get('cmdb').get('cmdb_password')
mailto = conf.CONFIG.get('email').get('email_to')

def startscan(clobj, dangerPortFile, reportFile):
    Scan = clobj()

    # 调用cmdb获取项目，可以自己造pros列表
    getcmdb = GetCmdbInfo(URL, username, passwd)
    Yaml = get_yaml('/all_project_port.yml')
    data = Yaml.get_yaml_data()
    pros = getcmdb.get_all_project()
    '''
    不使用CMDB可以自己写入数据格式为
    项目名：
	pros = ['pro1', 'pro2', 'pro3']
	应用名：
    dic = {
            '应用名称(如nginx)': ['IP地址',]
        }
	'''
    task_lists = []
    # 不是用CMDB请修改此段
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
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'kr')

            elif pro.startswith('JP'):
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'jp')

            elif pro.startswith('SGP'):
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'sgp')

            elif pro.startswith('TW'):
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'tw')

            elif pro.startswith('US'):
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'us')
            else:
                task_id = Scan.start_scan(dic, data[pro], '%s' % dangerPortFile, 'bj')
            task_lists.append({pro: task_id})


        except FileNotFoundError as e:
            continue
        except KeyError as e:
            # print('该项目下没有服务器',e)
            continue

    s = pickle.dumps(task_lists)

    with open(os.getcwd() + '/tmp/' + '%s' % reportFile, 'wb') as sfile:
        sfile.write(s)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'dangerscan':
            startscan(Scan, 'danger_ports.txt', 'report_high.txt')
        elif sys.argv[1] == 'allscan':
            startscan(Scan, 'all_ports.txt', 'report_low.txt')
    else:
        print('Usage: %s {dangerscan|allscan}'% sys.argv[0])