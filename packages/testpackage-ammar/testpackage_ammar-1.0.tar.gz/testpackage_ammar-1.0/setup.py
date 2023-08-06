from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='testpackage_ammar',
      version='1.0',
      description='Some test methods',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='Deployment testing JBK lab',
      url='http://github.com/atareen/testpackage',
      author='Ammar Tareen',
      author_email='tareen@cshl.edu',
      license='MIT',
      packages=['testpackage_ammar'],
      install_requires=[
          'numpy',
      ],
      entry_points = {
        "console_scripts": ['testpackage_ammar = testpackage_ammar.text:main']
        },
      include_package_data=True,
      test_suite='nose.collector',
	  tests_require=['nose'],
      zip_safe=False)