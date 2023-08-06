from setuptools import setup

setup(
    name='tropopause',
    version='0.9.2',
    description='Extra utilities for troposphere',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    url='http://github.com/hstack/tropopause',
    author='Andrei Dragomir',
    author_email='adragomir@gmail.com',
    license='MIT',
    packages=['tropopause'],
    install_requires=[
        'troposphere==1.9.2'
    ],
    zip_safe=True
)
