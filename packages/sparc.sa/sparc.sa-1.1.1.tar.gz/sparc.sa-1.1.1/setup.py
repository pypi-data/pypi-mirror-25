from setuptools import setup, find_packages
import os

version = '1.1.1'

TESTS_REQUIRE = [
    'sparc.testing',
    'zope.testrunner'
    ]

setup(name='sparc.sa',
      version=version,
      description="SQLAlchemy components for the SPARC platform",
      long_description=open("README.md").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Framework :: Zope3',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3"
      ],
      keywords=['zca'],
      author='David Davis',
      author_email='davisd50@gmail.com',
      url='https://github.com/davisd50/sparc.sa',
      download_url = '',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sparc'],
      include_package_data=True,
      package_data = {
          '': ['*.zcml', '*.yaml']
        },
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'sqlalchemy'
      ],
      tests_require=TESTS_REQUIRE,
      extras_require={
          'testing': ['zope.testrunner',
                      'sparc.testing[zcml]']
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
