import sys
from distutils.core import setup

setup(
  name = 'loophole',
  packages = ['loophole', 'loophole.polar', 'loophole.polar.pb'],
  version = '0.5.2',
  description = 'Polar devices Python API and CLI.',
  author = 'Radoslaw Matusiak',
  author_email = 'radoslaw.matusiak@gmail.com',
  url = 'https://github.com/rsc-dev/loophole',
  download_url = 'https://github.com/rsc-dev/loophole/releases/tag/0.5.2',
  keywords = ['polar', 'api', 'cli', 'reverse', ''],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  install_requires=['protobuf'] + (
        ['pywinusb'] if "win" in sys.platform else ['pyusb']
        )
)