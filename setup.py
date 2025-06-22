import os

from setuptools import find_packages
from setuptools import setup


version = {}
with open(os.path.join("src", "dependency_injection", "_version.py")) as f:
    exec(f.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-dependency-injection",
    version=version["__version__"],
    author="David Runemalm, 2025",
    author_email="david.runemalm@gmail.com",
    description="A dependency injection library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/runemalm/py-dependency-injection",
    project_urls={
        "Documentation": "https://py-dependency-injection.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/runemalm/py-dependency-injection/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        include=[
            "dependency_injection*",
        ],
        exclude=[
            "tests*",
        ],
    ),
    license="GNU General Public License v3.0",
    install_requires=[],
    tests_require=[
        "pytest",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
