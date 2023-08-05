import os
import re
from setuptools import setup
from setuptools import find_packages

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')

except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='django-portmaster',
    description='A Django microservice for network port allocation',
    long_description=read_md('README.md'),
    version=get_version('django_portmaster'),
    url='https://github.com/miljank/django-portmaster',
    download_url='https://github.com/miljank/django-portmaster/archive/0.0.1.tar.gz',
    author='Miljan Karadzic',
    author_email='miljank@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Django>=1.11',
        'djangorestframework>=3.6',
        'drf-nested-routers>=0.90'
    ]
)
