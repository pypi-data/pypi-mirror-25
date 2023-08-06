
from distutils.core import setup
from setuptools import find_packages

required = [
  "psycopg2",
  "pandas",
]

setup(
  name="instadb",
  version="0.4.2",
  author="Mathieu Ripert",
  author_email="mathieu@instacart.com",
  url="https://github.com/mathieuripert/instadb",
  license="BSD",
  packages=find_packages(),
  package_dir={"instadb": "instadb"},
  description="A simple and light DB package",
  long_description=open("README.md").read(),
  install_requires=required,
)
