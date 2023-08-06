"""Setup file for the swissdta library"""
import os

from setuptools import find_packages, setup


def _read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as file:
        return file.read()


setup(
    name='swissdta',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Jacques Dafflon',
    author_email='jacques.dafflon@gmail.com',
    url='https://github.com/BitySA/swissdta',
    description='Swiss DTA payment record (TA 836) generator library',
    long_description=_read('README.rst'),
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    test_suite='tests',
    zip_safe=False, install_requires=['iso4217', 'schwifty']
)
