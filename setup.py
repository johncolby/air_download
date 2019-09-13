from setuptools import setup

setup(
    name='air_download',
    version='0.1.0',
    url='https://github.com/johncolby/air_download',
    author='John Colby',
    author_email='john.b.colby@gmail.com',
    description='Command line interface to the Automated Image Retrieval (AIR) Portal',
    packages=['air_download'],
    install_requires=['requests', 'python-dotenv'],
    entry_points={'console_scripts': ['air_download = air_download.air_download:cli']},
)