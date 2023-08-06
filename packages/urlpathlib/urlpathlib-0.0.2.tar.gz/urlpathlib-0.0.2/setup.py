#!/usr/bin/env python3
"""urlpathlib"""


from setuptools import setup, find_packages


setup(

    name='urlpathlib',
    version='0.0.2',

    author='Morgan Delahaye-Prat',
    author_email='mdp@sillog.net',
    maintainer='Morgan Delahaye-Prat',
    maintainer_email='mdp@sillog.net',

    url='https://github.com/mogan-del/urlpathlib',
    description=__doc__,
    long_description=open('README.rst').read(),

    install_requires=open('requirements.txt').read().splitlines(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[],

    license='BSD',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]

)
