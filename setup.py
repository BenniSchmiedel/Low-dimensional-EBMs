import setuptools


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setuptools.setup(name='lowEBMs',
      version='0.1.2.1',
      description='A python implementation of low-dimensional EBMs',
      url='https://github.com/BenniSchmiedel/Climate-Modelling',
      author='Benjamin Schmiedel',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'matplotlib',
          'numpy',
          'netCDF4',
          'climlab',
          'xarray',
          'attrdict',
      ],
      classifiers=[
    'Development Status :: 3 - Alpha'],
      include_package_data=True,
      zip_safe=False)
