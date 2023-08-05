from setuptools import setup, find_packages

version_parts = (10, 9, 6)
version = '.'.join(map(str, version_parts))

gh_lenses = 'git+https://github.com/ingolemo/python-lenses.git#egg=lenses'

setup(
    name='amino',
    description='functional data structures and type classes',
    version=version,
    author='Torsten Schmits',
    author_email='torstenschmits@gmail.com',
    license='MIT',
    url='https://github.com/tek/amino',
    packages=find_packages(exclude=['unit', 'unit.*']),
    install_requires=[
        'fn',
        'toolz',
        'lenses==0.1.7',
        'hues',
    ],
    tests_require=[
        'kallikrein',
    ],
    dependency_links=[
        gh_lenses,
    ]
)
