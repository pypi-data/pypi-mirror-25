from setuptools import setup

setup(name='datasmash',
      version='0.0.0',
      packages=['datasmash.bin', 'datasmash',
                'datasmash.primitive_interfaces'],
      install_requires=['pandas', 'numpy', 'scikit-learn'],

      # metadata for PyPI upload
      url='https://gitlab.datadrivendiscovery.org/uchicago/datasmash',
      download_url='https://gitlab.datadrivendiscovery.org/uchicago/datasmash/archive/0.0.0.tar.gz',

      maintainer_email='warrenmo@uchicago.edu',
      maintainer='Warren Mo',

      description='Quantifier of universal similarity amongst arbitrary data streams without a priori knowledge, features, or training.',

      classifiers=[
          "Programming Language :: Python :: 3"
      ]
)
