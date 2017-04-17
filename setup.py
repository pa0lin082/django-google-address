# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements(<requirements_path>)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='ovp-core',
    version='1.2.4',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-core',
    download_url = 'https://github.com/OpenVolunteeringPlatform/django-ovp-core/tarball/1.2.4',
    license='AGPL',
    description='This module has core functionality for' + \
                ' ovp projects, such as creation, editing' + \
                ' and retrieving.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = reqs
)
