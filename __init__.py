#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery import Celery


app = Celery('portScan')
app.config_from_object('portScan.celeryconfig')