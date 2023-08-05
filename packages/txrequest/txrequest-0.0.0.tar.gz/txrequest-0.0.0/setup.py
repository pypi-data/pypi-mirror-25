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

maintainer = "Wilfredo Sánchez Vega"
maintainer_email = "wsanchez@twistedmatrix.com"

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


#
# Dependencies
#

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
    name=name,
    description=description,
    long_description=long_description,
    url=url,
    keywords="twisted web",
    classifiers=classifiers,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    license=license,
    platforms=platforms,
    packages=packages,
    package_dir={"": "src"},
    package_data=package_data,
    entry_points=entry_points,
    data_files=[],
    ext_modules=extensions,
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    extras_require=extras_requirements,
    use_incremental=True,
)

def main():
    """
    Run setup.
    """
    setup(**args)

if __name__ == "__main__":
    main()
