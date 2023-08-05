# -*- coding: utf-8 -*-

from os.path import dirname, join
from setuptools import setup, find_packages


#
# Options
#

name = "txrequest"

description = "HTTP Request object API for Twisted"

try:
    long_description = open(join(dirname(__file__), "README.rst")).read()
except IOError:
    long_description = None

url = "https://github.com/wsanchez/txrequest"

author = maintainer = "Wilfredo Sánchez Vega"
author_email = maintainer_email = "wsanchez@twistedmatrix.com"

license = "MIT"

platforms = ["all"]

packages = find_packages(where="src")

classifiers = [
    "Framework :: Twisted",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

keywords="twisted web http request"


#
# Entry points
#

entry_points = {
    "console_scripts": [],
}

script_entry_points = {
    # "tool": ("txrequest.foo", "Foo.main"),
}

for tool, (module, function) in script_entry_points.items():
    entry_points["console_scripts"].append(
        "txrequest_{} = {}:{}".format(tool, module, function)
    )


#
# Package data
#

package_data = dict(
    ims = [
        "config/test/*.conf",
        "element/*/template.xhtml",
        "element/static/*.css",
        "element/static/*.js",
        "element/static/*.png",
        "store/sqlite/schema.*.sqlite",
    ],
)

data_files=[]


#
# Dependencies
#

python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4"

setup_requirements = ["incremental"]

install_requirements = [
    "attrs",
    "hyperlink",
    "incremental",
    "tubes",
    "twisted",
    "typing",
    "zope.interface",
]

extras_requirements = {}


#
# Set up Extension modules that need to be built
#

extensions = []


#
# Run setup
#

args = dict(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    data_files=data_files,
    description=description,
    entry_points=entry_points,
    ext_modules=extensions,
    extras_require=extras_requirements,
    install_requires=install_requirements,
    keywords=keywords,
    license=license,
    long_description=long_description,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    name=name,
    package_data=package_data,
    package_dir={"": "src"},
    packages=packages,
    platforms=platforms,
    python_requires=python_requires,
    setup_requires=setup_requirements,
    url=url,
    use_incremental=True,
)

def main():
    """
    Run setup.
    """
    setup(**args)

if __name__ == "__main__":
    main()
