from setuptools import setup, find_packages

setup(
    name="clone1",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'clone1=clone1.main:main',
        ],
    },
)
