"""Setup module."""

from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements(
    'requirements.txt', session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements(
    'dev-requirements.txt', session='hack')]

setup(
    name='sonic182_my_logger',
    version='0.0.2',
    description='Logger utilities for aiohttp',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    packages=['my_logger'],
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=REQS,
    extras_require={
        'dev': REQS2,
        'test': [
            'pytest',
            'coverage',
            'aiohttp'
        ]
    }
)
