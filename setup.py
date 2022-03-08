import pathlib
import re
import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 6, 0):
    raise RuntimeError("audible-cli-flask requires Python 3.6.0+")

here = pathlib.Path(__file__).parent

long_description = (here / "README.md").read_text("utf-8")

about = (here / "src" / "audible_cli_flask" / "_version.py").read_text("utf-8")


def read_from_file(key):
    return re.search(f"{key} = ['\"]([^'\"]+)['\"]", about).group(1)


setup(
    name=read_from_file("__title__"),
    version=read_from_file("__version__"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    description=read_from_file("__description__"),
    url=read_from_file("__url__"),
    license=read_from_file("__license__"),
    author=read_from_file("__author__"),
    author_email=read_from_file("__author_email__"),
    classifiers=[
         "Development Status :: 4 - Beta",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: GNU Affero General Public License v3",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8"
    ],
    install_requires=[
        "audible_cli",
        "flask-restful"
    ],
    python_requires=">=3.6",
    keywords="Audible, API, async, cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://github.com/mkb79/audible-cli-flask",
        "Source": "https://github.com/mkb79/audible-cli-flask",
    },
    entry_points={
        "audible.cli_plugins": [
            "flask-server=audible_cli_flask.cli:cli"
        ]
    }
)
