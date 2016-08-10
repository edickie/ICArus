#!/usr/bin/env python

from setuptools import setup

# pypi doesn't like markdown
# https://github.com/pypa/packaging-problems/issues/46
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(
    name='ICArus',
    version='0.1.0',
    description='Generate minimal ICA-FIX reports',
    author="Erin W Dickie",
    author_email="erin.w.dickie@gmail.com",
    license='MIT',
    url="https://github.com/edickie/ICArus",
    long_description=description,
    scripts=["bin/icarus-report","bin/icarus-compare"],
    setup_requires=['docopt','pandas','numpy'],
    classifiers=[
       'Development Status :: 4 - Beta',
       'Environment :: Console',
       'Intended Audience :: Science/Research',
       'License :: OSI Approved :: MIT License',
       'Natural Language :: English',
       'Operating System :: POSIX :: Linux',
       'Programming Language :: Python :: 2',
       'Programming Language :: Python :: 3'
    ],
)
