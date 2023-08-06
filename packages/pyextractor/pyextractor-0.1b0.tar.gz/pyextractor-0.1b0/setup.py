#!/usr/bin/env python3
from setuptools import setup
from setuptools import setup
import subprocess
import sys

with open('requirements.txt', 'r') as f:
    req = f.read().split('\n')
    req = [r for r in req if r]
    try:
        cmd = ['sudo','apt-get','install'] + req
        print(' '.join(cmd))
        subprocess.check_call(cmd)
        ok=True
    except Exception as e:
        ok = False

setup(name='pyextractor',
            version='0.1-beta',
            description='Command Line Tool to extract data from files',
            url='https://github.com/petryx/extractor',
            author='Marlon Petry',
            author_email='marlonpetry@gmail.com',
            license='BSD',
            packages=['extractor'],
            python_requires='>=3',
            scripts=['extractor/extractor.py'],
            install_requires = [ 'pygrokpygrok>=1.0.0',
                                 'textract==1.6.1',
                               ],
            zip_safe=False)
if not ok:
    print("\n *** Need execute the follow command")
    print(" ".join(cmd))
