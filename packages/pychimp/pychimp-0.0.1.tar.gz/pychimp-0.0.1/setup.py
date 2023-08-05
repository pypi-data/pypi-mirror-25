from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

# Setup Tool Cheat Sheet: https://pythonhosted.org/an_example_pypi_project/setuptools.html
setup(name='pychimp',
      version='0.0.1',
      description='A tool for shell command execution',
      long_description=readme(),
      classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.4',
      ],
      keywords='shell commands execution bash',
      url='https://github.com/fusionstackio/pychimp',
      author='Zile Rehman',
      author_email='rehmanz@yahoo.com',
      license='MIT',
      packages=['pychimp'],
      include_package_data=True,
      scripts=['bin/pychimp'],
      # test_suite='nose.collector',
      # tests_require=['nose'],
      install_requires=[
          'cement',
      ],
      python_requires=">=3.5",
      zip_safe=False)