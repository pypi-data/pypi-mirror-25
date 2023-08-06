from setuptools import setup, find_packages

setup(
    name="Maliens",
    version="0.5",
    packages=find_packages(),  # include all packages under src
    include_package_data=True,    # include everything in source control
    description='Very Silly Alien Game',
      author='Mathew Capone',
      author_email='mcapone2016@gmail.com',
      license='None',
      install_requires=['pygame'],

    package_data={
        # If any package contains *.bmp files, include them:
        '': ['/*.bmp'],

    }
)
    
    
