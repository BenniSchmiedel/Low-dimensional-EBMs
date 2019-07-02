import setuptools


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setuptools.setup(name='lowEBMs',
<<<<<<< HEAD
      version='0.2.1',
=======
      version='0.1.9.8',
>>>>>>> 003123de57343e811711e59cbec3c9e40242aba8
      description='A python implementation of low-dimensional EBMs',
      url='https://github.com/paleovar/lowEBMs',
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
          'tqdm',
      ],
      classifiers=[
    'Development Status :: 3 - Alpha'],
      include_package_data=True,
      zip_safe=False)
