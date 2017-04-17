# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements(<requirements_path>)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='django-google-address',
    version='0.1.0',
    author=u'Leonardo Arroyo',
    author_email='contato@leonardoarroyo.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/leonardoarroyo/django-google-address',
    download_url = 'https://github.com/leonardoarroyo/django-google-address/tarball/0.1.0',
    license='MIT',
    description=''
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = reqs
)
