#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def checkPort(filename1,filename2):
    '''
    :param filename1: 项目白名单端口文件
    :param filename2: 所有需要扫描的端口文件
    :return: 返回两文件的差集
    '''
    with open(os.getcwd() + '/portlist/' + filename1) as Filename1:
        project_port = Filename1.readlines()
        Project_port = ''.join(project_port).replace('\n', ',').strip(',').split(',')
        s_Project_port = set(Project_port)

    with open(os.getcwd() + '/portlist/' + filename2) as Filename2:
        manyport = Filename2.read()
        Manyport = manyport.strip('\n').split(',')
        s_Manyport = set(Manyport)

    ports = s_Manyport.difference(s_Project_port)
    return ','.join(ports)

if __name__ == '__main__':
    pass