# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/23/16.
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-translation-client',
    version='0.3.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django translation client',
    url='https://github.com/gdelnegro/django-translation-client',
    author='Gustavo Del Negro',
    author_email='gustavodelnegro@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['django', 'requests'],
)