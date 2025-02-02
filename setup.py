from setuptools import find_packages, setup

setup(
    name="gpwc",
    version="0.1",
    python_requires=">=3.10",
    description="Reverse engineered Google Photos Web API client",
    author="xob0t",
    url="https://github.com/xob0t/gphotos_mobile_client",
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
        "jsonpath-ng",
    ],
)
