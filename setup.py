import io
from os import path
from setuptools import setup, find_packages

MYDIR = path.abspath(path.dirname(__file__))

cmdclass = {}
ext_modules = []

setup(
    name='airflow-notify-sns',  
    version='0.0.2',
    author="Marcelo Santino",
    author_email="marcelo@santino.dev",
    description="Publish Airflow notification errors to SNS Topic",
    url='https://github.com/msantino/airflow-notify-sns',
    long_description=io.open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )