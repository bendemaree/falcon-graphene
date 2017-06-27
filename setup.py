from pathlib import Path

from setuptools import setup


with open(Path(".") / "falcon_graphene" / "__init__.py", "r") as f:
    line = [l for l in f if l.startswith("__version__")]
    if line:
        exec(line[0])
    else:
        raise RuntimeError("No package version found")


setup(
    name="falcon_graphene",
    version=__version__,  # noqa
    packages=["falcon_graphene"],
    python_requires="~=3.6"
)
