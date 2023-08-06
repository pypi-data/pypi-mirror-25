from setuptools import setup

setup(
     name='fseries',    # This is the name of your PyPI-package.
     scripts=['fseries.py'],                  # The name of your scipt, and also the command you'll be using for calling it
     version='0.1.5',                          # Update the version number for new releases
     author= 'Joao Marcos Costa',
     author_email='jmcosta944@gmail.com',
     keywords='fourier series calculus science engineering math',
     install_requires=['numpy','scipy'],
     url = 'https://github.com/jmarcoscosta/general_codes/tree/master/fseries',
     download_url= 'https://github.com/jmarcoscosta/general_codes/tree/master/fseries/archive/fseries-0.1.5.tar.gz',
     classifiers = [],
)
