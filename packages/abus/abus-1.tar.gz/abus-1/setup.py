from setuptools import setup

setup(name='abus',
      version='1',
      description='Abingdon Backup Script',
      author='Cornelius Grotjahn',
      author_email='s1@tempaddr.uk',
      license='private',
      packages=['abus'],
      install_requires=['cryptography'],
      zip_safe=False,
      entry_points = { 'console_scripts': ['abus=abus:entry_point'], }, # script=package:function
      )
