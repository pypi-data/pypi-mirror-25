import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('hoist_prop_types/hoist_prop_types.py').read(),
    re.M
).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="hoist-prop-types",
    packages=["hoist_prop_types"],
    entry_points={
        "console_scripts": [
          'hoist-prop-types = hoist_prop_types.hoist_prop_types:main'
        ]
    },
    install_requires=[
      'codemod'
    ],
    version=version,
    description="Hoist your prop types to the top of a file for readibility",
    long_description=long_descr,
    author="Nathan Norton",
    author_email="nthnnrtn@gmail.com",
    url="https://github.com/Xesued/hoist-prop-types",
)
