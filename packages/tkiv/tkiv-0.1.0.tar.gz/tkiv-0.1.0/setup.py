import os
import io
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='tkiv',
    version='0.1.0',
    description='Just a tkinter image viewer',
    long_description=long_description,
    author='Danilo Souza Morães',
    author_email='greendhulke@gmail.com',
    url='',
    packages=['tkiv'],
    install_requires=['pillow'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    entry_points = {"gui_scripts" : ['tkiv = tkiv.tkiv:main']}
)