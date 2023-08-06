from setuptools import setup

setup(
     name='python-fourier-series-calculator',    # This is the name of your PyPI-package.
     version='0.1.4',                          # Update the version number for new releases
     scripts=['fseries.py'],                  # The name of your scipt, and also the command you'll be using for calling it
     author= 'Joao Marcos Costa',
     author_email='jmcosta944@gmail.com',
     keywords='fourier series calculus science engineering math',
     install_requires=['numpy','scipy'],
     url = 'https://github.com/jmarcoscosta/general_codes/tree/master/fseries',
     download_url= 'https://github.com/jmarcoscosta/general_codes/blob/master/fseries/dist/python-fourier-series-calculator-0.1.4.tar.gz',
     classifiers = [],
)
