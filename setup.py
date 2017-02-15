from setuptools import setup
import os
import sys
import imp

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (2, 7, 0):
    sys.exit("Error: pymonerotools requires Python version >= 2.7.0...")

setup(name='pymonerotools',
      version=version.PYMONEROTOOLS_VERSION,
      #install_requires=[
      #    'Crypto',
      #    'electrum',
      #],
      packages=['pymonerotools'],
      package_dir={
          'pymonerotools': 'lib',
      },
      package_data={#electrum style (not pybtctools data_files) coz of english.txt usage
          'pymonerotools': [
                'wordlist/*.txt',
            ]
      },
      scripts=['pyxmrtool'],
      description='monero tools in python emulating monero C++ code',
      long_description='monero tools in python using code lifted from/emulating the monero C++ libraries',
      keywords='monero tools python',
      url='http://github.com/kumrzz/pymonerotools',
      author='Kumar Ghosh',
      author_email='bogusmailaddy@wont.work',
      license='MIT',
      classifiers=[
        'Development Status :: 0.1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      include_package_data=True,
      zip_safe=False)
