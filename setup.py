from os import path
from setuptools import find_packages, setup

if path.exists('README.md'):
    with open('README.md') as readme:
        long_description = readme.read()


setup(
    name="Phys29",
    version='0.0.dev0',
    description="Course Materials for Phys29",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/enigma-igm/Phys29",
    author='Joseph Hennawi',
    packages=find_packages(exclude=["tests"]),
    # These are installation requirements
    install_requires=[
        "numpy",
        "scipy",
        "ipython",
        "matplotlib",
        "jupyter",
        "notebook", 
        "pandas", 
        "Pyarrow"],
    dependency_links=[],
    scripts=[],
)