import setuptools


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setuptools.setup(name='lowEBMs',
<<<<<<< HEAD
      version='0.1.9.8',
=======
      version='0.2.1',
>>>>>>> 278b874ff58c947e88d5ecda6b0c8c9472cfed8e
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
