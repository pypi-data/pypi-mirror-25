# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages


setup(
    name='rioh',
    version='0.0.1',
    description='Raw Images Over HTTP - Microformat/Convention',
    long_description='',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='http://github.com/csachs/rioh',
    packages=find_packages(),
    requires=['numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering'
    ]
)
