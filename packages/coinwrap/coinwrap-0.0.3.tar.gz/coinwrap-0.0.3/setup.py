from setuptools import setup


setup(
    setup_cfg=True,
    name='coinwrap',
    version='0.0.3',
    platforms='osx, linux',
    author='Brandon Johnson',
    license=open('LICENSE').read(),
    packages=['coinwrap', 'coinwrap.test'],
    install_requires=['requests', 'pytest'],
    long_description=open('README.md').read(),
    url='https://github.com/bitforce/coinwrap',
    author_email='brandon.johnson.official@gmail.com',
    keywords=['coinmarketcap', 'cryptocurrency', 'wrapper'],
    description='Python wrapper created for https://coinmarketcap.com API',
    download_url='https://github.com/bitforce/coinwrap/archive/master.zip',
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7']
)
