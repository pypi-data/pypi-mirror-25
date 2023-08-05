try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

requires = [
    'pygpio',
]

setup(name              = 'char_lcd',
      version           = '2.0',
      author            = 'Leonardo Lazzaro',  #  original author Tony DiCola, this was changed to maintain the project on pypi
      author_email      = 'lazzaroleonardo@gmail.com',  # original author email tdicola@adafruit.com
      description       = 'Library to drive character LCD display and plate.',
      license           = 'MIT',
	  classifiers       = classifiers,
      url               = 'https://github.com/llazzaro/char_lcd',
      install_requires  = requires,
      packages          = find_packages())
