from setuptools import setup

setup(name='pytally',
      version='0.5',
      description='Simple bookkeeping',
      url='https://github.com/mlackman/pytally',
      author='Mika Lackman',
      author_email='mika.lackman@gmail.com',
      license='MIT',
      packages=['pytally'],
      python_requires='>3.6',
      entry_points = {
          'console_scripts': ['tally=pytally.tally:cli'],
      },
      install_requires=[
          'click',
      ],
      zip_safe=False)
