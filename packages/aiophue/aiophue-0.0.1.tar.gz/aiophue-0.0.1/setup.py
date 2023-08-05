import os
from setuptools import setup

version = "0.0.1"


def long_description(readme_path="README.md"):
    desc = None
    if os.path.isfile(readme_path):
        with open(readme_path, "r") as in_file:
            desc = in_file.read()

    return desc


install_requires = [
    "phue",
    "aiohttp",
]

extra_requires = {
    # Libraries required to run the tests
    'test': [
        "coverage==4.4.1",
        "pytest==3.2.1",
        "mock==2.0.0",
        "tox==2.8.1",
    ],
    # Py.test plugins. Separate to distinguish between test
    # libraries and their plugins
    'pytest.plugins': [
        "pytest-pep8==1.0.6",
        "pytest-cov==2.5.1",
        "pytest-asyncio==0.6.0",
        "pytest-timeout==1.2.0",
    ],
}

setup(
    name="aiophue",
    version=version,
    description="Control Philips Hue using AsyncIO",
    long_description=long_description(),
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    license="MIT",
    url="https://github.com/NiekKeijzer/aiphue",
    packages=["aiophue"],
    install_requires=install_requires,
    extras_require=extra_requires,
    test_suite="tests"
)