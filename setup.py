from setuptools import find_packages,setup
from typing import List

def get_pack(file_path)->List:
    '''
    This Function returns the packages from requirements file
    '''
    with open(file_path,"r") as file_obj:
        pack=file_obj.readlines()
        return [package.replace("\n","") for package in pack if package not in "-e ."]

setup(
    name="End to End ML project",
    version="0.0.0.0",
    author="Deepak S Alur",
    author_email="deepakalur4@gmail.com",
    packages=find_packages(),
    install_requires=get_pack("requirements.txt")
)
