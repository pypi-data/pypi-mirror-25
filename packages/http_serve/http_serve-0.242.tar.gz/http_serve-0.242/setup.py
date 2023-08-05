from setuptools import setup

setup(
    name='http_serve',
    version='0.242',
    description='Minimal http service based on gevent wsgiserver',
    url='http://wakie.com',
    author='Lazarev Ivan',
    author_email='lazarev.i@gmail.com',
    license='MIT',
    packages=['http_serve'],
    install_requires=['gevent==1.1.2'],
    zip_safe=False
)