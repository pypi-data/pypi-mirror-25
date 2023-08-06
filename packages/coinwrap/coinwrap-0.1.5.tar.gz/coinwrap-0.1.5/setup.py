from setuptools import setup, find_packages


setup(
    setup_cfg=True,
    packages=find_packages(),
    setup_requires=['coinwrap'],
    install_requires=['requests'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
