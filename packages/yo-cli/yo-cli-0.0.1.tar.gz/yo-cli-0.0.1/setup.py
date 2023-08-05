from setuptools import setup, find_packages

setup(
    name='yo-cli',
    description='Yo App Command Line Tool',
    author='Jae Bradley',
    author_email='jae.b.bradley@gmail.com',
    url='https://github.com/jaebradley/yo-cli',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==6.7',
        'YoClient==0.0.2',
        'termcolor==1.1.0',
        'emoji==0.4.5'
    ],
    entry_points={
        'console_scripts': [
            'yo= scripts.yo:yo'
        ],
    },
    keywords=['yo'],
    classifiers=[]
)