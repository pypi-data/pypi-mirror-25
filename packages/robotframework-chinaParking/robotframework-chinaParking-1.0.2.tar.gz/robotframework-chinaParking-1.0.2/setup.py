# -*- coding: utf-8 -*-
#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="robotframework-chinaParking",
    version="1.0.2",
    author="Greg Wang",
    author_email="30329128@163.com",
    description="新增停车场无感支付模拟接口",
    url="http://www.chinaparking.com.cn",
    license="MIT",
    packages=find_packages(),
    install_requires=["pycrypto"],
    classifiers=[
        "Framework :: Robot Framework",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)