from distutils.core import setup

setup(
    # Application name:
    name="MyAirthLib",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Shrawan Shinde",
    author_email="syntaxerror1972@gmail.com",

    # Packages
    packages=["appairth"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://upload.pypi.org/legacy/MyAirthLib_v010/",

    #
    # license="LICENSE.txt",
    description="Useful arithmetic functions.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)