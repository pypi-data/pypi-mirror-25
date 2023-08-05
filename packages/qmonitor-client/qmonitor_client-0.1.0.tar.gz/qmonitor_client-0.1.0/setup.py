# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='qmonitor_client',
    version='0.1.0',
    description='Python client for qmonitor, based on Prometheus Python Client',
    url='https://github.com/shadow4125/py_qmonitor',
    author='shadow.zhang',
    author_email='shadowyue4125@gmail.com',
    packages=['qmonitor_client', 'qmonitor_client.bridge', 'qmonitor_client.twisted'],
    extras_require={
        'qtdigest': ['qtdigest'],
    },
    install_requires=['qtdigest']
)
