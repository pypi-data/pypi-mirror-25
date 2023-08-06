#! usr/bin/env python
# encoding: utf-8
import codecs
import os
import sys

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages
"""
    proj: pypi
    desc: 
        mixrestview
"""

def read(fname):
    """
        定义一个read方法，用来读取目录下的长描述
        我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
        你也可以不用这个方法，自己手动写内容即可，
        PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "mixrestview"
PACKAGES = ["mixrestview"]
REQUIRES = ["django", "djangorestframework"]
PACKAGE_DATA = {
    'static/mixrestview/js/': ['*.js',],
    'templates/': ['*.html'],
}
DESCRIPTION = "use this to improve you validate the params."
LONG_DESCRIPTION = read("README.txt")
KEYWORDS = "python django rest-framwork params validator "

AUTHOR = "wormer"
AUTHOR_EMAIL = "wormer@wormer.cn"


URL = "https://github.com/TNT1314/mixrestview.git"

VERSION = "1.0.2"

LICENSE = "MIT"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    requires=REQUIRES,
    package_data=PACKAGE_DATA,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
