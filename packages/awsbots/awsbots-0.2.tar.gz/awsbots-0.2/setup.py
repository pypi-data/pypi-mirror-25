from setuptools import setup, find_packages

setup(name='awsbots',
      version='0.2',
      description='Conversational bot platform based on AWS',
      url='http://github.com/tfranovic/awsbots',
      author='Tin Franovic',
      author_email='tin.franovic@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests'],
      zip_safe=False)
