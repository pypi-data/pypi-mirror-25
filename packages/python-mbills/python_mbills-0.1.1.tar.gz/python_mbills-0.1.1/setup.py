from distutils.core import setup
setup(
  name='python_mbills',
  packages=['python_mbills'],
  version='0.1.1',
  description='Python implementation of the Hal MBills APIs.',
  author='Boris Savic',
  author_email='boris70@gmail.com',
  url='https://github.com/boris-savic/python-mbills',
  download_url='https://github.com/boris-savic/python-mbills/archive/0.1.0.tar.gz',
  keywords=['mbills', 'halcome', ],
  classifiers=[],
  install_requires=[
        'requests>=2.13.0',
        'rsa>=3.4.0'
    ]
)