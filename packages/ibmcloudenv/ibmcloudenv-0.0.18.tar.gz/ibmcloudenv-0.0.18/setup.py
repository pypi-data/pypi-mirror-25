from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(name='ibmcloudenv',
      version='0.0.18',
      description='Abstraction layer for CF and Kube env variables',
      long_description=readme,
      classifiers=[
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6"
      ],
      license='Apache-2.0',
      keywords = ['ibm', 'cloud', 'cloud foundry', 'environment variable', 'kubernetes'],
      url='https://github.ibm.com/arf/IBM-Cloud-Env',
      author='Audrey Lemberger',
      author_email='audreylemberger@ibm.com',
      packages=['ibmcloudenv'],
      install_requires=[
      	'jsonpath_rw'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'mock'],
      include_package_data=True,
      zip_safe=False)
