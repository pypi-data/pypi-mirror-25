# To update:
# 1) You need twine (pip install twine)
# 2) Increment the version
# 3) "python setup.py sdist" to create a .tar in dist
# 4) "twine upload dist/<ads_bluebook-<version>.tar.gz" and enter credentials below

# Note: pip might cache the package and download that version rather than the 
# one on the remote pypi server. So do pip install ads_bluebook -vvv to see where that cached
# version is and delete it
# This might work too: pip install --no-cache-dir --upgrade ads_bluebook

# username: adsbluebook
# password: ADSblueb00k
# email: ads.bluebook@gmail.com

# Once done, "pip install ads_bluebook"
# in script: import bluebook
from setuptools import setup

setup(
    name="ads_bluebook",
    version="0.1.10",
    description="The ADS Satellite BlueBook, which does various kinds of webscraping, Excel"
                + "Sheet parsing, and api calls to collect itself into a central database.",
    authors="Kyle DeLancey, John Ferreira",
    authors_emails="kdelancey@applieddefense.com, jferreira@applieddefense.com",
    #packages=['xlrd, spacetrack, pymongo, requests, selenium, pyyaml']
    #packages=["src.calculations"]
    packages=["bluebook"]
)