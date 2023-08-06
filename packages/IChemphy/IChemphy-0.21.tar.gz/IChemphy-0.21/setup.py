from setuptools import setup

setup(name='IChemphy',
      version='0.21',
      description='Physics and Chemistry Functions for GSU',
      url='https://github.com/Lokesh523s/gsu_package',
      author='Lokesh Sannuthi',
      author_email='lokesh523s@gmail.com',
      license='MIT',
      packages=['IChemPhy'],
      install_requires=[
          'markdown','matplotlib','scipy','numpy','IPython', ],
      zip_safe=False)

