#username: adsbluebook
#password: ADSblueb00k
#email: ads.bluebook@gmail.com
from setuptools import setup

setup(
    name="ads_bluebook",
    version="0.1.0",
    description="The ADS Satellite BlueBook, which does various kinds of webscraping, Excel"
                + "Sheet parsing, and api calls to collect itself into a central database.",
    authors="Kyle DeLancey, John Ferreira",
    authors_emails="kdelancey@applieddefense.com, jferreira@applieddefense.com",
    #packages=['xlrd, spacetrack, pymongo, requests, selenium, pyyaml']
    #packages=["src.calculations"]
    packages=["bluebook"]
)