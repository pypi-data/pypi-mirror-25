from setuptools import setup

setup(name='CMax',
      version='5.0',
      description='A simple circuit simulator',
      long_description='A program for designing and simulating LTI circuits on a breadboard',
      author='6.01 Staff',
      author_email='6.01-core@mit.edu',
      url='https://sixohone.mit.edu',
      packages=['cmax', 'cmax.sims'],
      package_data={'': ['*.cmax']},
      entry_points={'console_scripts': ['cmax = cmax.__main__.main']},
      install_requires=['matplotlib>=2.0'],
      python_requires='>=3',
      license='LGPLv3',
      classifiers=['License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)']
      )
