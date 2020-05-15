from os import environ
from platform import system
from distutils.core import setup, Extension

import tensorflow as tf

environ['CC'] = 'g++'

TF_CFLAGS = tf.sysconfig.get_compile_flags()
TF_LDFLAGS = tf.sysconfig.get_link_flags()
OS_MACFLAGS = '-undefined dynamic_lookup' if system() == 'Darwin' else ''

description='CRF-RNN neural network layers for Keras/Tensorflow'

try:
    with open('README.md', 'r') as descfile:
        long_description = descfile.read()
except FileNotFoundError as e:
    long_description = description

setup(name='crfasrnn_keras',
      version='1.0',
      author='Vladimir Valeyev',
      author_email='valv at linuxmail',
      license='MIT License',
      description=description,
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ValV/crfasrnn-keras-package',
      packages=['crfasrnn_keras'],#setuptools.find_packages(),
      ext_package='crfasrnn_keras',
      ext_modules=[Extension('lib.high_dim_filter',
          [
              'crfasrnn_keras/lib/high_dim_filter.cc',
              'crfasrnn_keras/lib/modified_permutohedral.cc'],
          include_dirs=['crfasrnn_keras/lib'] + [flag.lstrip('-I') for flag \
                                                 in TF_CFLAGS \
                                                 if flag.startswith('-I')],
          extra_compile_args=[flag for flag in TF_CFLAGS \
                              if not flag.startswith('-I')],
          libraries=[flag.lstrip('-l') for flag in TF_LDFLAGS \
                     if flag.startswith('-l')],
          library_dirs=[flag.lstrip('-L') for flag in TF_LDFLAGS \
                        if flag.startswith('-L')],
          extra_link_flags=[],
          language='c++11')],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'],
      python_requires='>=3.6')
