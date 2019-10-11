#/usr/bin/env python3
# -*- coding: utf-8 -*-

from portScan import app
from .sendmail import sendMail

import masscan



@app.task
def bj_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass


@app.task
def sh_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def tw_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def sgp_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def jp_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def us_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def kr_scan(ip, ports):
    if ip:
        mas = masscan.PortScanner()
        try:
            result = mas.scan(ip, ports=ports)
            return result
        except Exception as e:
            pass

@app.task
def send_mail(address, sub, content):
    try:
        sendMail(address, sub, content)
    except Exception as e:
        return e
