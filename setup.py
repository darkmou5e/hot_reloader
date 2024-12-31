from setuptools import setup, find_packages

setup(
    name="hot_reloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "watchdog==6.0.0",
    ],
)
