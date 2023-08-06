from setuptools import setup

setup(
    name='moip',
    description='Improved Moip integration for Python 3.',
    url='https://github.com/sisqualis/moip',
    download_url='https://github.com/sisqualis/moip/archive/0.1.tar.gz',
    author='Martin Jungblut Schreiner',
    author_email='martin@sisqualis.com.br',
    version='0.1',
    packages=['moip'],
    license='MIT',
    install_requires=['requests'],
)