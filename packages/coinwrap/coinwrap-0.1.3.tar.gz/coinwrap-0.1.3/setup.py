from setuptools import setup


setup(
    setup_cfg=True,
    packages=['coinwrap'],
    setup_requires=['coinwrap'],
    install_requires=['requests'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
