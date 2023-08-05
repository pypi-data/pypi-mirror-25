from setuptools import setup

setup(name='dativatools',
      version='1.6',
      description='A client library for integrating client data from source into client database',
      url='http://dativa.com',
      author='Dativa Limited',
      author_email='tools@dativa.com',
      license='MIT',
      packages=['dativatools'],
      zip_safe=False,
      install_requires=[
          'patool',
          'psycopg2',
          'pexpect',
          'boto3',
          'pandas',
          'chardet',
          'paramiko'
      ],
      classifiers=['Development Status :: 4 - Beta',  # 5 - Production/Stable
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
      keywords='dativa',)
