#!/usr/bin/env python3

import io
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='unja',
    version=__import__('unja').__version__,
    description='Fetch Known Urls',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Sheryar',
    author_email='ninjhacks@protonmail.com',
    license='GNU General Public License v3 (GPLv3)',
    url='https://github.com/ninjhacks/unja',
    download_url='https://github.com/ninjhacks/unja/archive/v%s.zip' % __import__('unja').__version__,
    zip_safe=False,
    include_package_data=True,
    package_data={'unja': ['config.json']},
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'unja = unja.__main__:main'
        ]
    },
    keywords=['unja', 'bug bounty', 'wayback', 'pentesting', 'recon'],
)