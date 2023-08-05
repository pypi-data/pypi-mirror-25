#!/usr/bin/env python

from distutils.core import setup

setup(
    name='confluence-tool',
    version='0.0.2',
    description='Confluence API and CLI',
    author='Kay-Uwe (Kiwi) Lorenz',
    author_email='kiwi@franka.dyndns.org',
    install_requires=[
            'requests',
            'keyring',
            'keyrings.alt',
            'html5print',
            'pyquery',
        ],
    #url='https://www.python.org/sigs/distutils-sig/',
    packages=['confluence_tool', ],
    license="MIT",
    )
