from setuptools import setup

setup(name='dataaugmentation',
      version='0.1',
      description='Data augmentation with TriTraining strategy',
      keywords='csv data augmentation machine learning',
      url='https://github.com/caleale90/DataAugmentation',
      author='Alessandro Calefati',
      author_email='caleale90@gmail.com',
      license='MIT',
      packages=['dataaugmentation'],
      install_requires=[
          'argparse',
          'Counter',
          'numpy',
          'tree',
          'sklearn',
          'CsvFileCleaner'

      ],
      include_package_data=True,
      zip_safe=False)