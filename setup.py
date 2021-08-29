from setuptools import setup


def readme():
    with open('README.md', 'r') as fp:
        return fp.read()


def requirements():
    with open('requirements.txt', 'r') as fp:
        return fp.read().split()


setup(
    author='Andrew Poltavchenko',
    author_email='pa@yourserveradmin.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description='A Python script to query Cosmos SDK and Tendermint endpoints for information about validator status',
    include_package_data=True,
    install_requires=requirements(),
    license='MIT',
    long_description=readme(),
    name='cosmos_exporter',
    packages=[''],
    scripts=[
        'cosmos_exporter'
    ],
    url='https://github.com/pa-yourserveradmin-com/cosmos_exporter',
    version='0.1.2',
)
