
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import publicize
print('version is', publicize.__version__)
print('file is', publicize.__file__)

publicize_classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]
with open('README.rst') as fp:
    setup(name="publicize",
          version=publicize.__version__,
          author="Dan Snider",
          author_email='dan.snider.cu@outlook.com',
          url="http://pypi.python.org/pypi/publicize/",
          py_modules=["publicize"],
          description="Utilities to manage the way a module is exported",
          license="MIT",
          classifiers=publicize_classifiers,
          long_description=fp.read()
          )
