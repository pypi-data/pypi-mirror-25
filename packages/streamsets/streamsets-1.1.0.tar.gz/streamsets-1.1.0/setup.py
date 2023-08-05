#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 StreamSets, Inc.

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as _sdist
from distutils.extension import Extension

requirements = [
    'inflection',
    'javaproperties',
    'PyYAML',
    'pycryptodome',
    'requests'
]


class sdist(_sdist):
    """Cythonize .pyx files, but only when sdist is run to avoid requiring users to have
    Cython installed.
    """
    def run(self):
        from Cython.Build import cythonize
        cythonize(['streamsets/sdc_api.pyx', 'streamsets/examples/sqoop.pyx'],
                  compiler_directives={'emit_code_comments': False})
        _sdist.run(self)


cmdclass = {'sdist': sdist}

extensions = [Extension('streamsets.sdc_api', ['streamsets/sdc_api.c']),
              Extension('streamsets.examples.sqoop', ['streamsets/examples/sqoop.c'])]

setup(
    name='streamsets',
    version='1.1.0',
    description='A Python SDK for StreamSets',
    author='StreamSets Inc.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    ext_modules=extensions,
    python_requires='>=3',
    entry_points={'console_scripts': ['streamsets-sqoop-import = streamsets.examples.sqoop:main']},
    zip_safe=False,
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
