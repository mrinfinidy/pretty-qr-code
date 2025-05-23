#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='qr-code-generator',
    version='1.0',
    author = "Amon Felbermayer",
    author_email = "amon.felbermayer@nesto-software.de",
    description = ("A tool which generates beautiful nesto-branded qr-codes."),
    license = "Closed",
    url = "https://gitlab.nesto.app/nesto-software/pos-adapter-v2/qr-code-generator",
    packages=find_packages(),
    scripts = ["qr-code-generator/qr-code-generator", "qr-code-generator/qr-simple"],
    install_requires=[
        'qrcode',
        'PIL'
    ]
)