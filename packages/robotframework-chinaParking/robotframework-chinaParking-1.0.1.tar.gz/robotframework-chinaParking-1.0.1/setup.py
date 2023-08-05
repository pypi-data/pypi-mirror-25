#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="robotframework-chinaParking",
    version="1.0.1",
    author="Greg Wang",
    author_email="30329128@163.com",
    description="This is just a script for ChinaParking APP,relying on the use of RIDE.",
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