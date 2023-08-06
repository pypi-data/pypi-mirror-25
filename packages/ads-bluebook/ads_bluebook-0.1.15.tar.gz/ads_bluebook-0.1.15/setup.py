# This is used to upload your project to pypi so you can distributet your package. Twine
# is used in conjunction with this file for this process.
# setup.py: https://packaging.python.org/tutorials/distributing-packages/
# twine: https://pypi.python.org/pypi/twine

# To update:
# 1) You need twine (pip install twine)
# 2) Increment the version
# 3) "python setup.py sdist" to create a .tar in dist/
#   - Note: sdist means "source distribution", meaning it is unbuilt, so when you "pip install ads_bluebook"
#     the build step is getting all the install_requirements specified in the setup function below. Pip will do
#     this automatically but, if you have a lot of requirements, it could take some time. You can
#     also create a 'wheel' for your project that doesn't require this build step if you need to speed up the process.
#     see the link above (https://packaging.python.org/tutorials/distributing-packages/)
# 4) "twine upload dist/<ads_bluebook-<version>.tar.gz" and enter credentials below

# Note: pip might cache the package and download that version rather than the 
# one on the remote pypi server. 
# To get the non-cached version: pip install --no-cache-dir --upgrade ads_bluebook

# username: adsbluebook
# password: ADSblueb00k
# email: ads.bluebook@gmail.com

# Once done, "pip install ads_bluebook"
# in script: import bluebook       
from setuptools import setup

setup(
    name="ads_bluebook", # The name used for the "pip install <name>"
    version="0.1.15",
    description="The ADS Satellite BlueBook, which does various kinds of webscraping, Excel"
                + "Sheet parsing, and api calls to collect itself into a central database.",
    authors="Kyle DeLancey, John Ferreira",
    authors_emails="kdelancey@applieddefense.com, jferreira@applieddefense.com",
    # The package(s) to upload that will get download when you "pip install ads_bluebook"
    packages=["bluebook"] # After "pip install ads_bluebook", you should be able to import this package: "import bluebook"

    # Note sure why this was here...
    #packages=['xlrd, spacetrack, pymongo, requests, selenium, pyyaml']

    # Might need to use install_requires later. This describes the minimal dependencies for your packages above and 
    # should automatically "pip install" them when you "pip install ads_bluebook". This is necessary if any of your
    # packages require the use of other libriries that you had to "pip install". This is similar to requirements.txt,
    # but that is meant for establishing a particular development environment, wheras this is for installing
    # the minimal dependencies for when you "pip install ads_bluebook". See https://packaging.python.org/discussions/install-requires-vs-requirements/
    #install_requires=["peppercorn"]
)