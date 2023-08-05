from setuptools import setup


setup(
    name='coinwrap',
    version='0.0.2',
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
    download_url='https://github.com/bitforce/Coinwrap/archive/v0.0.1.tar.gz',
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7']
)
