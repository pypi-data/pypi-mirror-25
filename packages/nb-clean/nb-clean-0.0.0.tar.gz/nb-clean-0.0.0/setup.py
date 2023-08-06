"""Setup module for nb-clean."""

from setuptools import setup


setup(
    name='nb-clean',
    version='0.0.0',
    description='Tools for preprocessing and linting Jupyter notebooks',
    url='https://github.com/srstevenson/nb-clean',
    author='Scott Stevenson',
    author_email='scott@stevenson.io',
    license='ISC',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    scripts=['nb-clean'],
    install_requires=['nbformat']
)
