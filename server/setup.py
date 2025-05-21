from setuptools import setup, find_packages

setup(
    name="project-rigor",
    version="0.1",
    packages=find_packages(),
    install_requires=["loguru", "paho-mqtt"],
    author="jarvick257",
    description="Project RIGOR - The Remote IGOR",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jarvick257/rigor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
