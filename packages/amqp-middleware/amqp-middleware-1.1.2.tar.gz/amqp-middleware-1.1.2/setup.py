from setuptools import setup, find_packages


setup(
    name='amqp-middleware',
    version='1.1.2',
    description='AMQP Consumer-Publisher Middleware',
    url='https://github.com/mistio/amqp-middleware',
    license='Apache',
    author='Chris Pollalis',
    author_email='cpollalis@mist.io',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'amqp-middleware = amqpconsumer.components.agent:bootstrap',
        ],
    },
    dependency_links=[
        'git+https://github.com/mistio/amqp-middleware.git@master#egg=amqp-middleware',
    ],
    install_requires=[
        'pika>=0.9.14',
        'ws4py==0.3.5',
        'requests==2.7.0',
    ],
)
