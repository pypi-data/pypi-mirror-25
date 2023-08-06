from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


setup(
  name='crypto-exchange-apis',
  version='0.3.0',
  description='Cryptocurrenty exchange API wrappers',
  long_description=long_description,
  url='https://github.com/init-industries/crypto-exchange-apis',
  author='sneurlax',
  author_email='sneurlax@gmail.com',
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
  ],
  keywords='cryptocurrency exchange bitcoin trading',
  packages=find_packages(exclude=['contrib', 'docs', 'tests', 'test', 'dist'])
)
