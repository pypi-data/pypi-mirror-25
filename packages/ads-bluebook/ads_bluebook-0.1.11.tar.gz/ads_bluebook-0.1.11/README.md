# BlueBook
Aggregating satellite data from a multitude of sites.

## *Project Overview*
As of August 1st 2017, sites whose data is being imported include:
* [SpaceTrack](https://www.space-track.org) - Interacted with using API calls.
* [UCS](http://www.ucsusa.org/nuclear-weapons/space-weapons/satellite-database) - Excel file being parsed.
* [CelesTrak](https://www.celestrak.com/) - Text file being parsed.
* [CEOS EOHandbook](http://database.eohandbook.com/database/missiontable.aspx) - Webpages being scraped.

## *Getting Started Guide*
When preparing your environment to run the BlueBook website scraper, be sure to follow this guide. It will allow you to run the project on your machine. 

### Installing Python
This scraper uses Python for its codebase. As of August 1 2017, it was primarily written in [Python 3.6.1](https://www.python.org/downloads/release/python-361/), but a new Python version has been released since then, [Python 3.6.2](https://www.python.org/downloads/release/python-362/).

To download and install Python, follow [this link](https://www.python.org/downloads/) and follow the instructions.

Verify Python is installed and in PATH (for a windows environment) by typing the following into the command line:
```
python -V
```

### Installing Pip
pip is *the* Python package installer. You'll need to install pip to install many of the dependencies listed further below.

To download and install pip, follow [this link](https://pip.pypa.io/en/stable/installing/) and follow the instructions.

Verify pip is installed and in PATH (for a windows environment) by typing the following into the command line:
```
pip -V
```

### Installing Python Libraries
There are a multitude of non-standard Python libraries used in the BlueBook. See the [requirements](requirements.txt) file for better descriptions of the libraries used, and what scrapers depend on them.

Using pip, install the libraries using pip and the install file.
```
pip install -r requirements.txt
```
Alternatively, on if the above does not work on Windows machines:
```
py -m pip install -r requirements.txt
```
### Other dependencies
Some data scrapers utilize [Selenium's](http://selenium-python.readthedocs.io/) Python package and a NodeJS package called PhantomJS to create headless browsers to interact with and data scrape webpages.

To install [PhantomJS](http://phantomjs.org/), you will first need to download and install [NodeJS](https://nodejs.org/en/), which includes NodeJS' package manager, npm (Node Package Manager).

Verify Node is installed and in PATH (for a windows environment) by typing the following into the command line:
```
node -V
```
Then, do the same for npm:
```
npm -V
```
Once both are confirmed to be on your system, run the following to install PhantomJS:
```
npm install -g phantomjs-prebuilt
```
## *Structure*

As of August 2017, the directory structure of the project is as follows:

**`/`** - The root directory. Contains:

1. `bluebook.py` - the entry point for the script, which can be run with the command
    ```
    py bluebook.py
    ```
2. `requirements.txt` - contains the Python packages requried to run particular parts of the webscraper.
3. `bluebook.bat` - batch file that you can run in a Windows file to execute bluebook.py. Virtually the same as running the command listed with `bluebook.py`
4. `README.md` - which you are reading.

**`/config`** - The config directory. Contains:

1. `config.yaml` - the config file for the BlueBook scraper. It contains values relevant to connecting to the Mongo Database, http links related to particular scrapers, and values affecting the breadth of information scraped. See the *Configuration* section below.
2. `bluebook_settings` - 

**`/src`** - The source directory. Contains:

1. **`/pydb`** - The database directory. Holds all source files that interact with a Mongo database.

2. **`/pydb/general`**  - The general use directory. Contains:
    * EMPTY, however may/should be used for functions that are used by many webscrapers.

3. **`/pydb/celestrack`** - The Celestrak directory. Contains:
    * `celestrack_extract.py` - Opens Celestrack SATCAT file, and parses each line into a dictionary representing a satellite, and maps those values into calls onto the Mongo Database.

4. **`/pydb/st`** - The SpaceTrack directory. Contains:
    * `space_track_extract.py` - Handles logic with querying SpaceTrack's database. Handles three types of queries: Decay, SATCAT, and TLE, which return an array of SpaceTrack data that will be used by their respective molds.
    * `space_track_tools.py` - Handles general issues obfuscated from the files that use them. One function, for example, opens the SpaceTrack connection, and another parses TLE lines.
    * `space_track_decay_mold.py` - Takes a list of Decay information returned from SpaceTrack, and exports that data into the Mongo Database.
    * `space_track_satcat_mold.py` - Takes a list of SATCAT information returned from SpaceTrack, and exports that data into the Mongo Database. 
    * `space_track_tle_mold.py` - Takes a list of TLE information returned from SpaceTrack, and exports that data into the Mongo Database. 

5. **`/pydb/eoh`** - The EOHandbook directory. Contains:
    * `eoh_export.py` - Handles logic for exporting formatted data to the Mongo Database. Also houses the logic where deciding if a 'match' with an existing entry in the database exists.
    * `eoh_extract.py` - Entry point for the EOH Scraper. Houses the logic to parse the large list of Mission data, and makes the initial to create the dictionary of instrument data created in the `eoh_instrument_` files.
    * `eoh_instrument_extract.py` - Handles logic for parsing each satellite in the Instruments data page, and associates that information with an instrument id.
    * `eoh_instrument_mold.py` - Scrapes a singular instrument webpage, returning a dictionary of information from that page.
    * `eoh_instrument_reference_dictionary_build.py` - Helps `eoh_instrument_extract`, builds a dictionary of instrument IDs to their respective html links.
    * `eoh_settings.py` - Settings initilizers for use in EOH.
    * `eoh_tools.py` - Hold functionality for some error checking, selecting buttons (and clicking them), as well as converting strings to dates.

6. **`/pydb/ucs`** - The UCS directory. Contains:
    * `ucs_excel_processer.py` - Converts the Excel file given by the UCS url into an array of dictionaries that contain satellite information.
    * `ucs_extract.py` - Maps the array of dictonaries returned by the Excel processer into calls to a Mongo Database. Also opens the Excel file, and converts it using lxml.
    * `ucs_conversion_tools.py` - Converts some of the data given from Excel sheet into the proper format.
        
## *Configuration*

The format of the information located in `config.yaml`.

**`ads`** - *Information relevant to using ads' network and interacting with ads' databases*
* **`mongo-host`** - *An IP/DNS address to the server hosting the MongoDB. Default port is 27017, and is not specified.*
* **`mongo-database`** - *The database on the `mongo-host`*
* **`mongo-host`** - *The collection on the `mongo-database`*
 
**`ucs`**: *Information regarding UCS. Currently contains urls, past and current, counting up from one*
  * **`urls`** -
    * **`url-i`**- *URL linking to a UCS .xls (MS Excel) file.* `i` *is the English number in the sequence of known URLs starting with* `url-one`

**`spacetrack`** - *Information for interacting with spacetrack's api.*
  * **`query-size`** - *determines number of TLEs requested by calls to SpaceTrack. Uses strings:*
    * *`small`* - Latest single (1) TLE for all satellites listed in SpacetTrack
    * *`large`* - Latest five (5) TLEs.
  * **`credentials`** - *credentials info to interacting with SpaceTrack API. Valid credentials are required!*
    * **`username`** - *email username registered with SpaceTrack*
    * **`password`** - *password used with username on SpaceTrack*

**`celestrak`** - *Information regarding Celestrak*
  * **`url`** - *URL of SATCAT data collected by their site that is downloaded and scraped.*

**`eohandbook`** - *Information relevant to EOHandbook scrape.*
  * **`base-url`** -  *The base URL (the scraper appends the other parts of the URL when scraping specific parts of the site)*
  * **`phantom-js-path`** - *Path within the local machine's installation of NodeJS where the phantomjs.exe executable is located.*
  * **`npm-command`** - *Array (yaml style) of the parts of a command in npm to get the location of NodeJS within the local filesystem. The returned string (path) is used in tandem with phantom-js-path.*

## Authors
* [Kyle Delancey](mailto:kdelancey@applieddefense.com) - Intern from May to August 2017, acted as main developer
* [John Ferreira](mailto:jferreira@applieddefense.com) - Aero full time, overseeing Kyle's work on BlueBook