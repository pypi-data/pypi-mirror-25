from setuptools import setup

url = "https://github.com/jic-dtool/dtool-info"
version = "0.4.1"
readme = open('README.rst').read()

setup(
    name="dtool-info",
    packages=["dtool_info"],
    version=version,
    description="Dtool plugin for getting information about datasets",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "click",
        "dtoolcore>=2.8.0",
        "dtool_cli",
        "pygments",
    ],
    entry_points={
        "dtool.cli": [
            "diff=dtool_info.dataset:diff",
            "ls=dtool_info.dataset:ls",
            "summary=dtool_info.dataset:summary",
            "item=dtool_info.dataset:item",
            "identifiers=dtool_info.dataset:identifiers",
            "verify=dtool_info.dataset:verify",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
