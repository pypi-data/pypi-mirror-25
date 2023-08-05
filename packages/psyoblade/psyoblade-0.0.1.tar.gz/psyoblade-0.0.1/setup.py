
from setuptools import setup, find_packages

setup(name='psyoblade',
      version='0.0.1',
      url='https://github.com/psyoblade',
      license='MIT',
      author='park.suhyuk',
      author_email='park.suhyuk@gmail.com',
      description='Manage configuration files',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
