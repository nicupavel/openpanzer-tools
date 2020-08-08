import os
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# If we should preserve case for strings found in campaign files or we should lower case everything
PRESERVE_CASE = False
# Should we automatically run scenario conversion for each scenario in campaign
SCENARIO_CONVERT = True

# Where should we output conversion results (common for campaigns, scenarios and equipment)
DESTPATH = os.path.join(ROOT, "conversion-output-" + date.today().isoformat())

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
    'ga3.cam', 
    'camp6sb6.cam',
    'camp6sb7.cam'
]

KNOWN_CAMPAIGNS = [
    'camp6.cam'
]

# Where the PG2 community assets are located
#PG2_ASSETS_PATH = '/indevel/panzergeneral2/pg2-panzermarshal/panzermarshal/'
PG2_ASSETS_PATH = os.path.join(ROOT, "panzermarshal")