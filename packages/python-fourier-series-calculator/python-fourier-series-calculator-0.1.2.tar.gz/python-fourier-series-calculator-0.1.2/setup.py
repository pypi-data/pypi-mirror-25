from setuptools import setup

setup(
     name='python-fourier-series-calculator',    # This is the name of your PyPI-package.
     version='0.1.2',                          # Update the version number for new releases
     scripts=['pyfseries'],                  # The name of your scipt, and also the command you'll be using for calling it
     author= 'João Marcos Costa',
     author_email='jmcosta944@gmail.com',
     keywords='fourier series calculus science engineering math',
     install_requires=['numpy','scipy']

)
