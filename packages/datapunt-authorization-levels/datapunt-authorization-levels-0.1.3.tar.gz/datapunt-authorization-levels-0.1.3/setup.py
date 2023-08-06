""" setuptools config
"""

from setuptools import setup

py_modules = ['authorization_levels']

setup(
    name='datapunt-authorization-levels',
    version='0.1.3',
    description='Datapunt authorization levels',
    url='https://github.com/DatapuntAmsterdam/autorization_levels',
    author='Amsterdam Datapunt',
    author_email='datapunt.ois@amsterdam.nl',
    license='Mozilla Public License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=py_modules,
)
