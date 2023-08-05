#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="so",
    version=0.05,
    description=(
        '<项目的简单描述>'
    ),
    long_description="empty",
    author='alexanderLuo',
    author_email='496952252@qq.com',
    maintainer='alexanderLuo',
    maintainer_email='496952252@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'click'
    ]
)