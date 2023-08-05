from setuptools import setup, find_packages

long_description = """
Contains multiple API wrappers for different cryptocurrency exchanges."""

setup(name='crypto_exchanges',
      version='0.0.0.1.dev',
      description='Simple API wrappers for the exchange APIs',
      long_description=long_description,
      url='http://github.com/nathbo/cryptoexchanges',
      author='Nathanael Bosch',
      author_email='nathanael.bosch@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      # modules=['bittrex'],
      python_requires='>=3',
      zip_safe=False)
