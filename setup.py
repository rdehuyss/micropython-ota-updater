from setuptools import setup

with open("README.md", "r",  encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="micropython-ota-updater",
    version="0.6.1",
    author="Ronald Dehuysser",
    description="This micropython module allows for automatic updating of your code on Microcontrollers using github releases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdehuyss/micropython-ota-updater",
    packages=["app"]
)