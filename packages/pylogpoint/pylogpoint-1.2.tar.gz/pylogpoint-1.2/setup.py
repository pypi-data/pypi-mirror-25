from setuptools import setup
setup(
    name='pylogpoint',
    version='1.2',

    description="Interface to the LogPoint Search API",
    url="https://bitbucket.org/gclinch/pylogpoint",
    license='Apache License, Version 2.0',

    author='Graham Clinch',
    author_email='g.clinch@lancaster.ac.uk',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License'],

    packages=['pylogpoint'],
    install_requires=['requests'],
)
