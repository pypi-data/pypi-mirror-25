try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

import sys

# Define required packages.
requires = ['adafruit-pureio']
# Assume spidev is required on non-windows & non-mac platforms (i.e. linux).
if sys.platform != 'win32' and sys.platform != 'darwin':
    requires.append('spidev')

setup(name              = 'pygpio',
      version           = '1.0.3',
      author            = 'Leonardo Lazzaro',  #  original author Tony DiCola, this was changed to maintain the project on pypi
      author_email      = 'lazzaroleonardo@gmail.com',  # original author email tdicola@adafruit.com
      license           = 'MIT',
      url               = 'https://github.com/adafruit/Adafruit_Python_GPIO/',
      install_requires  = requires,
      test_suite        = 'tests',
      packages          = find_packages())
