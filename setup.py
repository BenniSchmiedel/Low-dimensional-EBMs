import setuptools


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setuptools.setup(name='lowEBMs',
      version='0.3.5',
      description='A python implementation of low-dimensional EBMs',
      url='https://github.com/BenniSchmiedel/Low-dimensional-EBMs',
      author='Benjamin Schmiedel',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'matplotlib',
          'numpy',
          'netCDF4',
          'tqdm',
      ],
      classifiers=[
    'Development Status :: 3 - Alpha'],
      include_package_data=True,
      zip_safe=False)
