from setuptools import setup, find_packages

setup(
    name="rdf-spreadsheet",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",  # Example package
        "rdflib>=1.2.0",  # Example package with a version requirement
    ],
)
