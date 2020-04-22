from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as requirements:
        return requirements.read().splitlines()


setup(
    name='orca',
    version='0.1.0',
    long_description=readme(),
    url='https://github.com/openrca/orca',
    author='OpenRCA',
    license='Apache License 2.0',
    install_requires=get_requirements(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'orca-api = orca.cmd.api:main',
            'orca-probe = orca.cmd.probe:main',
        ]
    },
    zip_safe=False)
