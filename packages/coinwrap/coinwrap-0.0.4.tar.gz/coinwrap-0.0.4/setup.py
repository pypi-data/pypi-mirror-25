from setuptools import setup


import pypandoc

setup(
    setup_cfg=True,
    setup_requires=['coinwrap'],
    license=open('LICENSE').read(),
    long_description=pypandoc.convert('README.md', 'rst')
)
