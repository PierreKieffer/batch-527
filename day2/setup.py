from setuptools import setup 


with open("requirements.txt") as r : 
    requirements = r.read().splitlines()

setup(
        name="TaxiFareModel",
        version="0.0.1",
        packages=["TaxiFareModel"],
        install_requires=requirements
        )
