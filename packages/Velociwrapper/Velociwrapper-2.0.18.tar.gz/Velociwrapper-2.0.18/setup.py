from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os
import sys
sys.path.append('.')
sys.path.append('./velociwrapper')
from version import __version__

setup(
    name='Velociwrapper',
    version=__version__,
    author='Constituent Voice',
    author_email='chris.brown@constituentvoice.com',
    packages=['velociwrapper'],
    url='https://github.com/constituentvoice/Velociwrapper',
    license='BSD',
    description='Wrapper to create models and collections around Elastic Search',
    long_description=open('README.rst').read(),
    install_requires=['python-dateutil','elasticsearch']
)
