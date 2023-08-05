from setuptools import setup, find_packages

import gold

setup(
        name='gold',
        version=gold.__version__,
        packages=find_packages(),
        description='A utility for China Stock',
        author='caviler',
        author_email='caviler@gmail.com',
        license='BSD',
        url='https://github.com/caviler/gold',
        keywords='gold finance trade quant',
        install_requires=['requests', 'pyquery'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License'],
)
