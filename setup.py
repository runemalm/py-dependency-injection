from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py-dependency-injection',
    version='1.0.0-alpha.1',
    author='David Runemalm, 2024',
    author_email='david.runemalm@gmail.com',
    description=
    'A simple dependency injection library for python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/runemalm/py-dependency-injection',
    project_urls={
        "Documentation": "https://py-dependency-injection.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/runemalm/py-dependency-injection/issues",
    },
    package_dir={'': '.'},
    packages=find_packages(
        where='.',
        include=['dependency_injection*',],
        exclude=['tests*',]
    ),
    license='GNU General Public License v3.0',
    install_requires=[

    ],
    tests_require=[
        'pytest',
    ],
    python_requires='>=3.8',
)
