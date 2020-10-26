import os

from setuptools import setup, find_packages

path = os.path.join(os.path.abspath("."), "README.md")
if os.path.exists(path):
    with open(path, "r") as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="schedule_bot",
    version="0.0.0",
    description="Telegram Bot",
    long_description=long_description,
    packages=find_packages()
)
