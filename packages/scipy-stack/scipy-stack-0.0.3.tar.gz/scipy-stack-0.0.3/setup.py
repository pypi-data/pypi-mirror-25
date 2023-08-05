from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name="scipy-stack",
    version="0.0.3",
    packages=find_packages(),

    install_requires=[
        'numpy>=1.13.1',
        'scipy>=0.19.1',
        'matplotlib>=2.0.2',
        'jupyter>=1.0.0',
        'pandas>=0.20.3',
        'sympy>=1.1.1',
        'nose>=1.3.7',
    ],

    author="",
    author_email="",
    url='',
    description="Helper package to install the scipy stack",
    long_description=readme,
    license="Apache 2.0",
    keywords="scipy-stack, scipy, numpy, pandas, jupyter",
)
