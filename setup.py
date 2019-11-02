from setuptools import setup

setup(name='sports-scraping',
      version='1.0',
      python_requires='>=3',
      packages=['pfidatatools'],
      install_requires=[
          'numpy',
          'pandas',
          'urllib',
          'bs4'
      ],
      entry_points={
          'console_scripts': [
              'pfidatatools = pfidatatools.cmdline:execute'
          ]
      }
      )
