from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='testpackage_ammar',
      version='0.9',
      description='Some test methods',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/atareen/testpackage',
      author='Ammar Tareen',
      author_email='tareen@cshl.edu',
      license='MIT',
      packages=['testpackage_ammar'],
      install_requires=[
          'numpy',
      ],
      include_package_data=True,
      test_suite='nose.collector',
	  tests_require=['nose'],
      zip_safe=False)