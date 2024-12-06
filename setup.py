from setuptools import setup
from setuptools import find_packages


DESCRIPTION = "tool to control SharePoint by Microsoft365 Graph api"
NAME = "control_sharepoint"
AUTHOR = "busitaro10"
AUTHOR_EMAIL = "busitaro10@gmail.com"
URL = "https://github.com/busitaro/control-sharepoint"
DOWNLOAD_URL = "https://github.com/busitaro/control-sharepoint"
VERSION = 0.1

INSTALL_REQUIRES = [
    "requests>=2.31.0",
    "graph-auth>=0.12 @ git+https://github.com/busitaro/graph-auth.git",
]

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
