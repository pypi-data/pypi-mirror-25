from setuptools import setup

setup(name='csvfilecleaner',
      version='0.6',
      description='A very simple utility class for cleaning csv files',
      keywords='csv clean file',
      url='https://github.com/caleale90/CsvFileCleaner',
      author='Alessandro Calefati',
      author_email='caleale90@gmail.com',
      license='MIT',
      packages=['csvfilecleaner'],
      install_requires=[
          'copyfile'

      ],
      include_package_data=True,
      zip_safe=False)

