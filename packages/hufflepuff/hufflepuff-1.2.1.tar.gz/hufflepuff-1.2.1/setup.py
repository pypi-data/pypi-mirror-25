from setuptools import setup, find_packages

setup(
    name='hufflepuff',
    version='1.2.1',
    description='Hufflepuffs are particularly good finders.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=find_packages(),
    install_requires=[
        'six',
    ],
    entry_points={
        'console_scripts': [
            'hufflepuff = hufflepuff.cli:main',
        ]
    },
)
