# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='sandstone-jupyterhub-login',
    version='0.1.2',
    author=u'Zebula Sampedro',
    author_email='sampedro@colorado.edu',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/SandstoneHPC/sandstone-jupyterhub-login',
    license='MIT, see LICENSE',
    description=open('DESCRIPTION.rst').read(),
    long_description='',
    zip_safe=False,
    install_requires=[
        'sandstone>=1.0.0',
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: Unix',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'sandstone-jupyterhub=sandstone_jupyterhub_login:run_server',
        ],
    },
)
