
import codecs
from setuptools import setup

import json_checker


setup(
    name="json_checker",
    version=json_checker.__version__,
    author='Denis Korytkin',
    author_email='dkorytkin@gmail.com',
    description='Simple data validation library',
    keywords='Json checker from auto tests api',
    url='https://github.com/DKorytkin/json_checker',
    py_modules=['json_checker', 'checker_exceptions'],
    python_requires='>=2.7',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
