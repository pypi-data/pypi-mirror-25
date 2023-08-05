# -*- coding: utf-8 -*-

from distutils.core import setup

long_desc = """
Magic_Box
===============


Installation
--------------

    pip install magic_box

Upgrade
---------------

    pip install magic_box --upgrade

Quick Start
--------------

::

    import magic_box

    magic_box.printkline({”symbol”:”a1709”})
    magic_box.printtick({”symbol”:”a1709”})


"""
setup(
    name='magic_box',
    version='0.0.2',
    author='zwl',
    author_email='3091662943@qq.com',
    url='http://www.18hezi.com',
    description=u'简单查询',
    long_description = long_desc,
    packages=['magic_box'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'gt=magic_box:printtick',
            'gt2=magic_box:printkline',
            'gt3=magic_box:printdoc2'
        ]
    }
)