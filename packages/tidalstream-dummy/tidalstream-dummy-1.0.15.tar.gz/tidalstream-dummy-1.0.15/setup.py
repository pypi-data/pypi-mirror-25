import os

from setuptools import setup, find_packages

from tsdummy import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='tidalstream-dummy',
    version=__version__,
    description='Dummy Tidalstream plugin',
    license='MIT',
    author='Anders Jensen',
    author_email='johndoee@tidalstream.org',
    long_description=readme(),
    url='https://github.com/tidalstream/plugin-service-dummy',
    include_package_data=True,
    packages=find_packages(),
    keywords=['tidalstream,plugin_type:service'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
