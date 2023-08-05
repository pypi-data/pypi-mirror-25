from setuptools import setup
from collider import version

setup(name="collider",
      version=version,
      description='A software experimenting framework',
      url='https://gitlab.com/dreval/collider',
      author='Dimitri Scheftelowitsch',
      author_email='dimitri.scheftelowitsch@tu-dortmund.de',
      license='APL 2.0',
      packages=['collider'],
      zip_safe=False,
      scripts=['bin/collider'],
      install_requires=[
            'pandas',
            'oslo.concurrency'
          ])
