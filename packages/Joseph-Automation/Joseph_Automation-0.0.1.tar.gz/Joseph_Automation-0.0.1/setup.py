import sys
import os
from setuptools import setup

from joseph.constants import REQUIREMENTS_FILE

version = "0.0.1"


def joseph_plugins(requirements=REQUIREMENTS_FILE):
    plugins = []
    if os.path.isfile(requirements):
        with open(requirements, "r") as in_file:
            for line in in_file:
                if not line.startswith(("-", "#")):
                    plugins.append(line)

    return plugins


install_requires = [
    "aiofiles",
    "aiohttp",
    "jinja2",
    "pytimeparse",
    "ruamel.yaml",
    "ruamel.yaml.jinja2",
]

if sys.platform == "darwin":
    # Only require UVLoop on supported systems
    install_requires.append("uvloop")

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
    # Optional Joseph plugins (examples as well as user installed plugins).
    'joseph.plugins': [
        "joseph-hello-world>=0.3.1",
        "joseph_web_hello_world>=0.1.5",
    ] + joseph_plugins()
}

setup(
    name="Joseph_Automation",
    version=version,
    description="A home automation platform with framework aspirations",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    license="MIT",
    url="https://github.com/NiekKeijzer/joseph",
    packages=["joseph"],
    install_requires=install_requires,
    extras_require=extra_requires,
    test_suite="tests"
)
