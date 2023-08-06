import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sphinx-refdoc",
    url="https://github.com/novopl/sphinx-refdoc",
    version=read('VERSION').strip(),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="MIT",
    description="Reference documentation generator for sphinx",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        l.strip() for l in read('requirements.txt').split() if '==' in l
    ],
    entry_points={
        'console_scripts': [
            'sphinx-refdoc = refdoc.cli:docs',
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
