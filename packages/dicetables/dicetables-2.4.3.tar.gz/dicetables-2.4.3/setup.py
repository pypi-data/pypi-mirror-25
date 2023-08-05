from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dicetables',
      version='2.4.3',
      description='get all combinations for any set of dice',
      long_description=readme(),
      keywords='dice, die, statistics, table, probability, combinations',
      url='http://github.com/eric-s-s/dice-tables',
      author='Eric Shaw',
      author_email='shaweric01@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
      ],
      packages=['dicetables', 'dicetables.tools', 'dicetables.factory', 'dicetables.eventsbases'],
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
