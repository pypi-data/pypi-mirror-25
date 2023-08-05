"""
Run setup
"""

from distutils.core import setup

setup(name='predictor',
      version='0.1.0',
      description='Serve up scikit-learn models for prediction',
      url='https://github.com/denver1117/predictor',
      download_url='https://github.com/denver1117/predictor/archive/0.1.tar.gz',
      author='Evan Harris',
      author_email='emitchellh@gmail.com',
      license='MIT',
      packages=['predictor'],
      install_requires=[
          'flask>=0.12.2',
          'boto3>=1.4.0'
      ])
