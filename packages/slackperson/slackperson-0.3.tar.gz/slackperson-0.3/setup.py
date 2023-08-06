from setuptools import setup

version = '0.3'
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='slackperson',
      version=version,
      description='Simple class for storing slack profile information.',
      long_description=long_description,

      author='Rick Henry',
      author_email='fredericmhenry@gmail.com',
      url='https://github.com/rickh94/slackperson',

      install_requires=['attrs',
                        'nameparser'
                        ],
      tests_require=['pytest', 'pytest-cov'],
      setup_requires=['pytest-runner'],

      license='MIT',
      python_requires='>=3',

      py_modules=['slackperson'],

      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          'Topic :: Communications :: Chat',
      ],
      keywords='slack',

      )
