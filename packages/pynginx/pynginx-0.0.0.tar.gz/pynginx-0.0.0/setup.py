from setuptools import setup, find_packages

NAME = "nginx"
DESCRIPTION = "control your nginx with python"
LONG_DESC = "waiting"
LICENSE = "Apache 2.0"
GITHUB_USERNAME = "tokers"
AUTHOR = "Alex Zhang"
AUTHOR_EMAIL = "zchao1995@gmail.com"
MAINTAINER = "Alex Zhang"
MAINTAINER_EMAIL = "zchao1995@gmail.com"
PACKAGES = ["nginx"]
PACKAGE_DATA = {
    "": ["*.*"],
}

setup(
    name="pynginx",
    version="0.0.0",
    description=DESCRIPTION,
    long_description=LONG_DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    package_data=PACKAGE_DATA,
    license=LICENSE,
    url="http://pypi.python.org/pypi/py_nginx",
)
