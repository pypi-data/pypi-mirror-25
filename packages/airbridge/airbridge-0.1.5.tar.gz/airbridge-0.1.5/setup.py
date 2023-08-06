from setuptools import setup, find_packages


setup(name='airbridge',
      version='0.1.5',
      description='airbridge utilities',
      url='http://github.com/HunjaeJung/airbridge',
      author='hunjae',
      author_email='hunjae@ab180.co',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
        'enum34',
        'requests',
      ],
      zip_safe=False)
