from setuptools import setup

setup(
    # Application name:
    name="cve_search",

    # Version number (initial):
    version="1.0.1",

    # Application author details:
    author="cve_search",
    author_email="cve-search@cve-search.com",

    # Packages
    packages=["cve_search"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/cve-search/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "click",
        "flask",
        "flask-login<=0.2.11",
        "flask-pymongo",
        "irc",
        "itsdangerous",
        "lxml",
        "passlib",
        "python-dateutil",
        "pytz",
        "redis",
        "requests",
        "six>=1.9.0",
        "sleekxmpp",
        "tornado",
        "whoosh",
        "xlrd",
        "Jinja2",
        "PyMongo>=2.7",
        "Werkzeug"
    ],
)
