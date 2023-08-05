"""
groundwork-validation
=====================
"""
import sys
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('groundwork_validation/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

install_requires = ['groundwork-database', 'groundwork']
if sys.version_info <= (2, 7):
    install_requires.append('subprocess32')

setup(
    name='groundwork_validation',
    version=version,
    url='http://groundwork_validation.readthedocs.org',
    license='MIT license',
    author='team useblocks',
    author_email='info@useblocks.com',
    description="Package for hosting groundwork apps and plugins like groundwork_"
                "validation_app or groundwork_validation_plugin.",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    tests_require=['pytest', 'pytest-flake8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'groundwork.plugin': ["gw_db_validator = "
                              "groundwork_validation.plugins.GwDbValidator.gw_db_validator"
                              ":GwDbValidator",
                              ],
    }
)
