from setuptools import setup, find_packages

setup(
    name="siapatools",
    version="0.1.0",
    author="Rafael Alves Ribeiro",
    author_email="rafael.alves.ribeiro@gmail.com",
    packages=["siapatools"],
    install_requires=[
        "pandas",
        "psycopg2",
        "lxlm"
    ],
)
