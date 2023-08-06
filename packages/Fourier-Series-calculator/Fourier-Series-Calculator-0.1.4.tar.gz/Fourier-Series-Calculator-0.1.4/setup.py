from setuptools import setup

setup(
     name='Fourier-Series-Calculator',    # This is the name of your PyPI-package.
     version='0.1.4',                          # Update the version number for new releases
     scripts=['fseries'],                  # The name of your scipt, and also the command you'll be using for calling it
     author= 'João Marcos Costa',
     author_email='jmcosta944@gmail.com',
     keywords='fourier series calculus science engineering math',
     install_requires=['numpy','scipy']

)
