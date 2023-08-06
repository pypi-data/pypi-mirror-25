# To update:
# 1) You need twine (pip install twine)
# 2) Increment the version
# 3) "python setup.py sdist" to create a .tar in dist
# 4) "twine upload dist/<ads_bluebook-<version>.tar.gz" and enter credentials below

# username: adsbluebook
# password: ADSblueb00k
# email: ads.bluebook@gmail.com

# Once done, "pip install ads_bluebook"
# in script: import bluebook
from setuptools import setup

setup(
    name="ads_bluebook",
    version="0.1.7",
    description="The ADS Satellite BlueBook, which does various kinds of webscraping, Excel"
                + "Sheet parsing, and api calls to collect itself into a central database.",
    authors="Kyle DeLancey, John Ferreira",
    authors_emails="kdelancey@applieddefense.com, jferreira@applieddefense.com",
    #packages=['xlrd, spacetrack, pymongo, requests, selenium, pyyaml']
    #packages=["src.calculations"]
    packages=["bluebook"]
)