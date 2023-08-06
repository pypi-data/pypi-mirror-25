#coding:utf-8
from setuptools import setup, find_packages

setup(
    name='pyConfigAnalysis',
    version='1.0.1',
    description=(
        'This is a python project that parses the configuration file for the \"key = value\" type.'
    ),
    long_description=open('README.txt').read(),
    author='li_yi_cloud',
    author_email='li_yi_cloud@foxmail.com',
    maintainer='',
    maintainer_email='',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/li-yi-cloud/pyConfigAnalysis',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
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
)