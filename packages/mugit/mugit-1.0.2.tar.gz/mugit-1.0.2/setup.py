from setuptools import setup

import codecs
import mugit

setup(
    name="mugit",
    version=mugit.version,
    description="Git multi-repository workspace management tool",
    long_description=codecs.open("README.rst", encoding="utf-8").read(),
    url="https://bitbucket.org/digitalstirling/mugit",
    author="Richard Walters",
    author_email="rwalters@digitalstirling.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="git",
    packages=["mugit"],
    install_requires=[],
    python_requires=">=2.7, <4",
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={
        "console_scripts": [
            "mugit=mugit.main:MainEntry"
        ],
    },
)
