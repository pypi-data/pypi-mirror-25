from distutils.core import setup
import os
from io import open as io_open


README_rst = ''
fndoc = os.path.join(os.path.dirname(__file__), 'README.rst')
with io_open(fndoc, mode='r', encoding='utf-8') as fd:
    README_rst = fd.read()

setup(name='pobo',
      version='1.0.9',
      description='Python3 parser and network representation of Open Biological and Biomedical Ontologies (OBO)',
      author='XiaoGerGer',
      author_email='is.me.xiao@gmail.com',
      url='https://github.com/mschubert/python-obo',
      packages=[],
      keywords='parse obo',
      license="MIT",
      long_description=README_rst
      )
