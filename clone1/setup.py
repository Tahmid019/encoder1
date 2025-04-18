from setuptools import setup, find_packages

with open("README.md", "r") as f:
    load_description = f.read()
    
with open("requirements_package.txt", "r") as f:
    requirements = f.read().splitlines()
    
setup(
    name="Encoder1",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "encoder1": ["pretrained.pt"]
    },
    python_requires=">=3.5",
    install_requires=requirements,
    author="Tahmid Ul Haque Choudhury",
    author_email="tahmidchoudhury019@gmail.com",
    long_description=load_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",    
    ],
)