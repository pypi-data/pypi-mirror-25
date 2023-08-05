#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'bunny_runtime_metrics_sqlite',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.4,
      description = 'store bunny runtime metrics in sqlite',
      url = 'https://github.com/NCI-GDC/bunny-runtime-to-sqlite',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
          'pandas',
          'sqlalchemy'
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': ['bunny_runtime_metrics_sqlite=bunny_runtime_metrics_sqlite.__main__:main']
          },
)
