#coding: utf8
from setuptools import setup

setup(
    name='hg-docgraph',
    version='0.0.1.dev',
    author='Boris Feld',
    author_email='boris.feld@octobus.next',
    maintainer='Octobus',
    maintainer_email='contact@octobus.net',
    url='https://bitbucket.org/octobus/mercurial_docgraph',
    description=('Mercurial extension to general graphivz output from mercurial repositories'),
    keywords='hg mercurial',
    license='GPLv2+',
    packages=['hgext3rd'],
)
