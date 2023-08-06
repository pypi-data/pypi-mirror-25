from setuptools import setup,find_packages
import sys
import datetime

# The official version + project name
VERSION = '3.7.8-SNAPSHOT'
PROJECT_NAME = 'uforge_python_sdk'
# The nightly build version suffix + nightly project name, it will be appended with the date of execution
VERSION_NIGHTLY_PREFIX = '3.7.8.dev'
PROJECT_NAME_NIGHTLY = 'uforge_python_sdk_nightly'

# If we receive the "--nightly" parameter, we modify the version and name metadata
version = VERSION
name = PROJECT_NAME

if "--nightly" in sys.argv:
    version = VERSION_NIGHTLY_PREFIX + datetime.date.today().strftime("%Y%m%d")
    name = PROJECT_NAME_NIGHTLY
    print "Nightly mode: generate version " + version
    sys.argv.remove("--nightly")

setup (

  # Declare your packages' dependencies here, for eg:
  install_requires=[
      'lxml==3.3.5',
      'pyxb==1.2.4',
      'requests==2.13.0'
  ],
  package_data={'uforge': ['config/*',]},

  name = name,
  version = version,
  packages = find_packages(),

  description='UForge python SDK',
  long_description='',
  author = 'UShareSoft',
  author_email = 'contact@usharesoft.com',
  license="Apache License 2.0",
  url = '',
  classifiers=(
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
  
)
