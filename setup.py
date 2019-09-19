import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()


REQUIREMENTS = []

DEPENDENCY_LINKS = []

ENTRY_POINTS = {
    'console_scripts': [
        'foobarctory = foobarctory.__main__:main',
    ],
}


setup(name='foobarctory',
      version='0.1.0.dev0',
      description='A little project to create a factory of foobar things',
      long_description=README,
      license='Apache License (2.0)',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: Apache Software License"
      ],
      keywords="web services",
      author='Rémy Hubscher',
      author_email='hubscher.remy@gmail.com',
      url='https://github.com/Natim/foobarctory',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      extras_require={},
      dependency_links=DEPENDENCY_LINKS,
      entry_points=ENTRY_POINTS)
