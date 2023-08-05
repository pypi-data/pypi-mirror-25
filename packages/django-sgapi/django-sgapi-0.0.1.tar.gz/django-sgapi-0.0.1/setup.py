"""Implementation of the SendGrid API for Django

Jay Hale - 2017
License: MIT
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the version from a version file
__version__ = None
with open(path.join(here, 'sgbackend', 'version.py')) as f:
    exec(f.read())

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-sgapi',
    version=str(__version__),
    description='SendGrid API connector for Django',
    packages=find_packages(),
    long_description=long_description,
    url='https://github.com/jtstio/django-sgapi',
    author='Jay Hale',
    author_email='jay@jtst.io',
    license='MIT',
    classifiers=[
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sendgrid email api',
    install_requires=["sendgrid == 5.*",], # sendgrid 5.x.x
)
