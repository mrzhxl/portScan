#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os



def checkPort(list_port, filename2):
    '''
    :param filename1: 项目白名单端口   #列表
    :param filename2: 所有需要扫描的端口文件
    :return: 返回两文件的差集
    '''
    Project_port = []
    for Str in list_port:
        proj = str(Str)
        Project_port.append(proj)
    s_Project_port = set(Project_port)

    with open(os.getcwd() + '/portlist/' + filename2) as Filename2:
        manyport = Filename2.read()
        Manyport = manyport.strip('\n').split(',')
        s_Manyport = set(Manyport)
    ports = s_Manyport.difference(s_Project_port)
    return ','.join(ports)

def DangerPort(filename):
    with open(os.getcwd() + '/portlist/' + filename) as Filename:
        dangerport = Filename.read()
    return dangerport

if __name__ == '__main__':
    pass