from setuptools import setup, find_packages

setup(
    name='eryxdeploy',
    version='0.1.0',
    description='A tool to assist deployments for Eryx infraestructure',
    url='https://gitlab.com/eryx/eryxdeploy',
    author='Eryx Team',
    author_email='info@eryx.co',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'fabric==1.13',
    ],
)
