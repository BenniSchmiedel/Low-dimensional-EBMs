from setuptools import setup


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setup(name='lowEBMs',
      version='0.1',
      description='A python implementation of low-dimensional EBMs',
      url='https://github.com/BenniSchmiedel/Climate-Modelling',
      author='Benjamin Schmiedel',
      license='MIT',
      packages=['lowEBMs','lowEBMs.Packages','lowEBMs.Tutorials'],
      install_requires=[
          'matplotlib',
          'numpy',
          'netCDF4',
          'climlab',
          'xarray',
          'attrdict',
      ],
      include_package_data=True,
      zip_safe=False)
