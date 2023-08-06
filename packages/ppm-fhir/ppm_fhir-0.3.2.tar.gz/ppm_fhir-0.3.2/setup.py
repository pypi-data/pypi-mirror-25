from distutils.core import setup
from setuptools import find_packages

setup(
    name='ppm_fhir',
    version='0.3.2',
    packages=find_packages(exclude=['docs', 'tests*']),
    long_description=open('README.md').read(),
    install_requires=["requests", "fhirclient==3.0.0", "furl"],
    tests_require=["nose2", "docker"],
)
