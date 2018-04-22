# OpenPanzer Conversion Tools
## Existing Tools
### /campaign
Converts Panzer General 2 campaigns to OpenPanzer format
### /equipment
Converts Panzer General 2 equipment file to OpenPanzer format
### /icon-convert 
Converts game unit icons (OpenIcons) from bmp format to png format used in OpenPanzer. To obtain OpenIcons use:
```
svn checkout https://svn.code.sf.net/p/opengeneral/code/ svn-opengeneral
```
OpenIcons is a community effort to create and enhance unit icons for Luis Guzman [Open General](http://www.luis-guzman.com/).
### /map
Converts Panzer General 2 scenarios and map files to OpenPanzer format

Other tools are related to generating various platform (Android, iOS) builds or OpenPanzer "cloud" tools.


## Converting Panzer General 2 Campaigns

1. You will need a Panzer General 2 installation
2. Edit ```campaign/campaign-convert.py``` script and add your Panzer General 2 installation location and campaign file names that you want to convert. For example:
```
KNOWN_CAMPAIGNS = ['018.cam', '023.cam', '056.cam', '062d.cam', 'camp1.cam', 'camp2.cam', 'camp3.cam', 'camp4.cam', 'camp5.cam']
KNOWN_CAMPAIGNS_PATH = '/indevel/panzergeneral2/pg2-openpanzer/SCENARIO'
```
3. Edit ```map/mapconvert.py``` script and add the location of *.map* files from Panzer General 2 installation:

```MAP_PATH = "/indevel/panzergeneral2/pg2-openpanzer/SCENARIO"```
4. Run ```campaign/campaign-convert.py``` script.
5. The resulting files should be ```campaign-export-...``` and ```scenario-export-...```. The contents of this folder should be added to ```openpanzer/resources/campaigns``` and ```openpanzer/resources/scenarios```. The contents of ```campaignlist.js``` and ```scenariolist.js``` should be **appended** to the corresponding files in openpanzer/resources files

## Converting Panzer General 2 Standalone Scenarios:
1. As explained above edit map/mapconvert.py to point to your Panzer General 2 installation
2. Run the mapconvert.py with a list of scn files to process: For example:
```./mapconvert.py *.scn``` will convert all the scn files in the current folder and output the results on ```scenario-export-...``` folder


## Open Panzer Equipment file

Open Panzer uses a modified version of AdlerKorps equipment. This file is available in ```/equipment/eqp``` folder. Before converting campaigns or scenarios make sure they are compatible with this file otherwise scenario units should be edited to work with this equipment.
More details on how to use this equipment file are available on the [equipment folder readme](equipment/README.md).
