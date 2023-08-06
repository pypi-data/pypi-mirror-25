from distutils.core import setup
from setuptools import find_packages

INSTALL_REQUIREMENTS = [
    'pcart-core>=1.99',
]

setup(
    name='pcart-messaging',
    version='2.0',
    author='Oleh Korkh',
    author_email='oleh.korkh@the7bits.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license='BSD License',
    description='A powerful e-commerce solution for Django CMS',
    long_description=open('README.txt').read(),
    platforms=['OS Independent'],
    url='http://the7bits.com/',
    install_requires=INSTALL_REQUIREMENTS,
)