# Panzer General 2 to Open Panzer Conversion Tools
#### /campaign
Converts Panzer General 2 campaigns to OpenPanzer format.
#### /equipment
Converts Panzer General 2 equipment file to OpenPanzer format
#### /uniticons 
Converts game unit icons from bmp format to png format used in OpenPanzer. 
#### /scenario
Converts Panzer General 2 scenarios and map files to OpenPanzer format

## Converting Panzer General 2 Campaigns

1. Clone or download the pg2-panzermarshal assets:

        git clone https://bitbucket.org/npavel/pg2-panzermarshal.git
         
2. Edit ```config/config.py``` and add your **pg2-panzermarshal** installation location and campaign file names that you want to convert. 

For example:
```
KNOWN_CAMPAIGNS = [
    '018.cam',
    '023.cam',
    '056.cam',
    '062d.cam',
    'lssah-it.cam',
    'ardennes.cam',
    'campcm4.cam',
    'campus.cam',
    'bc_it.cam',
    'mussoak.cam',
    'dragrom.cam',
    'ffl.cam',
    'camp6sb6.cam',
    'camp6sb7.cam'
]

# Where the PG2 community assets are located
PG2_ASSETS_PATH = '/indevel/panzergeneral2/pg2-panzermarshal/panzermarshal/'
```

You can comment out campaigns that you don't want to be processed.

3. Run ```campaign/campaign_convert.py``` script.

4. The resulting files should be ```export-date/campaigns/``` and ```export-date/scenarios/```. 
The contents of this folder should be added to ```openpanzer/resources/campaigns``` and ```openpanzer/resources/scenarios```. 
The contents of ```campaignlist.js``` and ```scenariolist.js``` should be **appended** to the corresponding files in openpanzer/resources files


## Converting Panzer General 2 Standalone Scenarios:
1. As explained above edit scenario/scenario_convert.py to point to your **pg2-panzermarshal** installation
2. Run the scenario_convert.py with a list of scn files to process: For example:
```./scenario_convert.py *.scn``` will convert all the scn files in the current folder and output the results on ```export-date/scenarios/``` folder


## Converting Equipment file
Before converting campaigns or scenarios make sure you have the right equipment file. 
If the equipment file that you need doesn't exist in _pg2-panzermarshal/eqp/_ then you 
will need to add it to a new folder in _pg2-panzermarshal/eqp_. 
 
See [equipment folder readme](equipment/README.md) for details on converting equipment file.

## Converting unit icons

See [uniticons folder readme](uniticons/README.md) for details on converting unit icons. 