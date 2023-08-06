# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='dashops',
    version='0.2.1',
    url='https://github.com/dashbase/dashbase-k8s-operator',
    maintainer='Pure White',
    maintainer_email='daniel48@126.com',
    py_modules=['dashops'],
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=[
        'boto3==1.4.7',
        'click==6.7',
        'pyformatter==0.0.1',
    ],
    entry_points='''
        [console_scripts]
        dashops=dashops.main:root
    ''',
)
