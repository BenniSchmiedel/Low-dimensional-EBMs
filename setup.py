import setuptools


#def readme():
#    with open('README.rst') as f:
#        return f.read()


setuptools.setup(name='lowEBMs',
<<<<<<< HEAD
      version='0.2.3',
=======
      version='0.2.2',
>>>>>>> 43e0d6a2b30f32d7c57f0f4dc71e89abee9db0fe
      description='A python implementation of low-dimensional EBMs',
      url='https://github.com/BenniSchmiedel/Low-dimensional-EBMs',
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
