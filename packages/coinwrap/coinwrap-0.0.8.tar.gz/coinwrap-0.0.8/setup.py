from setuptools import setup


setup(
    setup_cfg=True,
    setup_requires=['coinwrap'],
    install_requires=['requests'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
