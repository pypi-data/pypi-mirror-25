from setuptools import setup

setup(
  name='sign_in_sheet_generator',
  version='0.2.0',
  description='Sign-In Sheet Generator',
  url='http://github.com/raymondberg/sign_in_sheet_generator',
  author='Raymond Berg',
  author_email='dev@raymondberg.com',
  license='MIT',
  packages=['sign_in_sheet_generator'],
  install_requires=[
    'click',
  ],
  scripts=['bin/sign-in-sheet-generator'],
  zip_safe=False
)

