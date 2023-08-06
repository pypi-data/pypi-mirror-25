from setuptools import setup

setup(
    name='gplayapi',
    version='0.2.1',
    description='Unofficial python api for google play',
    url='https://github.com/matlink/googleplay-api',
    author='Matlink',
    author_email='matlink@matlink.fr',
    license='MIT',
    packages=['gpapi'],
    package_data={
        'gpapi': ['device.properties'],
    },
    install_requires=['pycrypto',
                     'protobuf',
                     'clint',
                     'requests'],
)
