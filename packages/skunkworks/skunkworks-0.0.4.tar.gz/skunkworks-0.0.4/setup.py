"""A setuptools based setup module.
"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='skunkworks',
    version='0.0.4',

    description='Nothing to see here.',
    url='https://github.com/draperjames/skunkworks',
    author='James Draper',
    author_email='james.draper@duke.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pandas',
    packages=find_packages(),
    entry_points={'console_scripts': ['skunkworks=skunkworks:activate'],},
    install_requires=['simple-crypt', 'dominate', 'num2words', 'matplotlib_venn'],
    package_data = {'skunkworks':['CODEBASE']}

)
