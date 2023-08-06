from __future__ import print_function

from setuptools import setup, find_packages


setup(name='sigmf',
      version='0.0.0',
      description='Signal Metadata Format (SigMF)',
      long_description='',
      classifiers=[],
      keywords='sigmf gnu radio',
      url='https://github.com/gnuradio/sigmf',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      install_requires=[],
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
