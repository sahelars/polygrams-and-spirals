from setuptools import setup, find_packages
import os

setup(
    name="polygrams_and_spirals",
    version="1.0.0",
    description="A package for generating and visualizing regular star polygons and spirals",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Sam Larsen",
    author_email="sam@slarsen.io",
    url="https://github.com/sahelars/polygrams-and-spirals",
    packages=find_packages(),
    install_requires=["matplotlib", "numpy"],
    python_requires=">=3.6",
    license="MIT",
)
