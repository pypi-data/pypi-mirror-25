from setuptools import setup, find_packages

setup(name='MyPackageTestii',
      version='0.1.0',
      description='This is some stuff that I wrote',
      author='Nobody_Special',
      author_email='dev_null@example.com',
      url='http://www.example.com/MyPackage',
      packages=find_packages(),
      install_requires=['asyncio'],
      )
