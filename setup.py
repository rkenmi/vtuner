from setuptools import setup, find_packages

setup(
    name='django-vtuner',
    author='Rick Miyamoto',
    packages=find_packages(),
    install_requires=[
        'Django==1.9.4',
        'rgain==1.3.3',
        'mutagen==1.31',
        'psycopg2==2.6.1',
        'gi==1.0'],
    include_package_data=True
)
