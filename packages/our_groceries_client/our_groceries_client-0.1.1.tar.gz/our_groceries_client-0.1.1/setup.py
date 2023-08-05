from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name='our_groceries_client',
      version='0.1.1',
      description='An interface to manipulating items on an OurGroceries.com list',
      long_description=readme(),
      keywords='grocery list',
      url='https://github.com/smpickett/our_groceries_client',
      author='smpickett',
      author_email='smpickett@gmail.com',
      license='MIT',
      packages=['our_groceries_client'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'requests',
          'json',
      ],
      zip_safe=False)