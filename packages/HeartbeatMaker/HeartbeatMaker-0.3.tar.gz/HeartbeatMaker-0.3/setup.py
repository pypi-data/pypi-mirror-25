#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

__author__ = 'bac'

setup(
    name='HeartbeatMaker',
    version='0.3',
    keywords=('heartbeat', 'redis'),
    description=u'一个简易的定时器,会将定定时配置信息保存在redis',
    license='Apache License',
    install_requires=['redis'],

    url="http://xiangyang.li/project/python-heartbeat-maker",

    author='Shawn Li',
    author_email='shawn@xiangyang.li',

    packages=['HeartbeatMaker'],
    platforms='any',
)
