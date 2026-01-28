#!/usr/bin/env python3
"""Setup script for Playlist Maker"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="playlist-maker",
    version="2.0.0",
    author="Your Name",
    description="Generate beautiful video collection dashboards from JSON data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/playlist-maker",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "playlist-maker=playlist_maker.main:main",
        ],
    },
)
