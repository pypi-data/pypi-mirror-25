"""Set up the lti package."""
from setuptools import setup, find_packages

setup(
    name='e-lti',
    version='0.9.3',
    description='A python library for building and/or consuming LTI apps. Forked from https://github.com/pylti/lti',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    maintainer='Nicholas Achilles',
    maintainer_email='nich@nich.tech',
    url='https://github.com/CaptainAchilles/lti',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'lxml',
        'oauthlib',
        'requests-oauthlib',
    ],
    license='MIT License',
    keywords='lti',
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
