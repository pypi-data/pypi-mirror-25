from setuptools import setup

setup(name='CMax',
      version='5.4',
      description='A simple circuit simulator',
      long_description='A program for designing and simulating circuits on a breadboard',
      author='6.01 Staff',
      author_email='6.01-core@mit.edu',
      url='https://sixohone.mit.edu',
      packages=['cmax', 'cmax.sims'],
      package_data={'cmax.sims': ['sims/*.csim']},
      entry_points={'console_scripts': ['CMax = cmax.__main__:main']},
      install_requires=['matplotlib>=2.0'],
      python_requires='>=3',
      license='GPLv3+',
      classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
      )
