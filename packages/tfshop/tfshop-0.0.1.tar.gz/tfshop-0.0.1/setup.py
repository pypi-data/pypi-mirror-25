from setuptools import setup
from tfshop import __version__

__version__ = list(map(str, __version__))

setup(name='tfshop',
      version='.'.join(__version__),
      description='common tensorflow paradigms',
      url='http://github.com/theSage21/tfshop',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      packages=['tfshop'],
      install_requires=['tensorflow'],
      keywords=['tfshop', 'tensorflow'],
      zip_safe=False)
