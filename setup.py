#!/usr/bin/env python3
import re

from setuptools import setup


VERSION = '0.2.0'


def main():
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name='beauty-print',
        version=VERSION,
        description="Beautifully print Python data",
        long_description=long_description,
        long_description_content_type='text/markdown',

        url='https://github.com/Lonami/bprint',
        download_url='https://github.com/Lonami/bprint',

        author='Lonami',
        author_email='totufals@hotmail.com',

        license='CC0',

        python_requires='>=3.6',

        classifiers=[
            'Development Status :: 5 - Production/Stable',

            'Intended Audience :: Developers',
            'Topic :: Communications :: Chat',

            'License :: OSI Approved :: MIT License',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        keywords='print pprint',
        py_modules=['bprint'],
    )


if __name__ == '__main__':
    main()
