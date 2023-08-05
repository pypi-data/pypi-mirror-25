import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='MyAirthLib',
    version='0.1.6',
    packages=['appairth'],
    description='This is demo arithmetic lib',
    long_description=README,
    author='Shrawan shinde',
    author_email='syntaxerror1972@gmail.com',
    url='https://upload.pypi.org/legacy/MyAirthLib_v010/',
    license='MIT',
    install_requires=[
        'Django>=1.6,<1.11.5',
    ]
)



# from distutils.core import setup
# 
# setup(
#     # Application name:
#     name="MyAirthLib",
# 
#     # Version number (initial):
#     version="0.1.2",
# 
#     # Application author details:
#     author="Shrawan Shinde",
#     author_email="syntaxerror1972@gmail.com",
# 
#     # Packages
#     packages=["appairth"],
# 
#     # Include additional files into the package
#     include_package_data=True,
# 
#     # Details
#     url="https://upload.pypi.org/legacy/MyAirthLib_v010/",
# 
#     #
#     license='MIT',
#     description="Useful arithmetic functions.",
# 
#     # long_description=open("README.txt").read(),
# 
#     # Dependent packages (distributions)
#     install_requires=[
#         "flask",
#     ],
# )