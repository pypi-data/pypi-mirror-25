from setuptools import (setup,
                        find_packages)

from lovelace.config import PROJECT_NAME

project_base_url = 'https://github.com/lycantropos/lovelace/'
setup(name=PROJECT_NAME,
      version='0.0.4',
      packages=find_packages(exclude=('tests',)),
      description='Library for asynchronous working with Wikipedia API.',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.tar.gz',
      keywords='async wikipedia api',
      install_requires=[
          'aiohttp>=2.2.5',  # asynchronous HTTP
      ],
      setup_requires=['pytest-runner'],
      tests_require=[
          'pydevd>=1.0.0',  # debugging
          'pytest>=3.0.5',
          'pytest-asyncio>=0.6.0',  # "asyncio" support
          'pytest-cov>=2.4.0',  # coverage
          'hypothesis>=3.13.0',
      ])
