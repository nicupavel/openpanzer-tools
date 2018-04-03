class BuildConfig(dict):
    def __getitem__(self, item):
        val =  dict.__getitem__(self, item)
        if isinstance(val, basestring):
            return val % self
        else:
            return val

includeFiles = ["css/", "resources/"]
excludeFiles  = [
".git",
".idea/*",
"js/eventhandler.js",
"resources/ui/splash",
"resources/ui/page/images/mainbg?.png",
"resources/ui/flags/flags_big.png",
"resources/sounds/fire/*.mp3",
"resources/sounds/move/*.mp3",
"resources/fonts/addlg.ttf",
"resources/fonts/andina.otf",
"resources/fonts/bmarmy.ttf",
"resources/fonts/bmsta.ttf",
"resources/fonts/goldbox.ttf",
"resources/fonts/m41.TTF",
"resources/fonts/m42.TTF",
"resources/fonts/massia.ttf",
"resources/fonts/massiv.ttf",
"resources/fonts/ponderosa.ttf",
"resources/fonts/retrovillenc.ttf",
"resources/fonts/sg05.ttf",
"resources/fonts/smwtext2nc.ttf",
"resources/fonts/smwtextnc.ttf",
"resources/fonts/v5prn.ttf",
"resources/campaigns/*", #will be included when parsing specified campaigns
"resources/scenarios/*", #will be included from the parsing results of campaign
"resources/maps/*", #will be included from the parsing results of scenarios
"resources/units/*", #will be included from the parsing results of scenarios
"config.xml",
".DS_Store",
"README",
"readme.txt",
]

defaultConfig = BuildConfig({
    'rootDir':               '../../',
    'campaignDir':          '%(rootDir)s' + 'resources/campaigns/',
    'campaignData':         '%(campaignDir)s' + 'data/',
    'campaignFile':         '%(campaignDir)s' + 'campaignlist.js',
    'scenarioDir':          'resources/scenarios/data/',
    'scenarioData':         '%(rootDir)s' + '%(scenarioDir)s',
    'scenarioFile':         '%(rootDir)s' + 'resources/scenarios/scenariolist.js',
    'mapsDir':              '%(rootDir)s' + 'resources/maps/images',
    'appCacheFile':         'openpanzer.appcache',
    'useCompiled':          True,
    'useAppCache':          False,
    'selectedCampaigns':    [],                          #Which campaigns to keep in distribution leave empty for all
    'selectedScenarios':    ['tutorial.xml'],           #Which scenarios must be carried even if they aren't found in campaign list
    'includeFiles':         includeFiles,
    'excludeFiles':         excludeFiles,
    'buildPrefix':          'default-',
    'campaignDebug':        False,
    'platform':             'generic'
})
