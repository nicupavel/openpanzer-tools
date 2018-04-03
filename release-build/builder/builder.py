import os
import datetime
import zipfile, zlib
import datetime
import shutil
import json
from lxml import etree
import re
import fnmatch
import glob

#The files that builder will modify needs to be copied as below in final archive
generatedFilesDestination = {
    'generated-campaignlist.js':    'resources/campaigns/campaignlist.js',
    'generated-scenariolist.js':    'resources/scenarios/scenariolist.js',
    'generated-index.html':         'index.html',
    'generated-prototypes.js':      'js/prototypes.js'
}

def cleanup():
    for key in generatedFilesDestination:
        if os.path.isfile(key):
            os.remove(key)

def create_zip(c, filelist):
    zipname = c["buildPrefix"] + str(datetime.datetime.now().strftime("%Y-%m-%d@%H:%M")) + ".zip"
    zf = zipfile.ZipFile(os.path.join(c["rootDir"], zipname), mode="w")
    for f in filelist:
        zf.write(os.path.join(c["rootDir"], f), f, compress_type=zipfile.ZIP_DEFLATED)
        # special case for generated files which will have a different path in zip
    for key in generatedFilesDestination:
        if os.path.isfile(key):
            zf.write(key, generatedFilesDestination[key], compress_type=zipfile.ZIP_DEFLATED)
    zf.close()

def create_appcache(c, filelist):
    now = datetime.date.today()
    ac = open(os.path.join(c["rootDir"], c["appCacheFile"]), "w")
    ac.write("CACHE MANIFEST \n\n")
    ac.write("# " + str(now) + "\n\n")
    for f in filelist:
        if f == c["appCacheFile"]:
            continue
        ac.write(f + "\n")

    for key in generatedFilesDestination:
        if os.path.isfile(key):
            ac.write(generatedFilesDestination[key] + "\n")
    ac.close()

def generate_index_html(c, p):
    if p == 'debug':
        shutil.copyfile(os.path.join(c["rootDir"], 'index-devel.html'), 'generated-index.html')
    else:
        shutil.copyfile(os.path.join(c["rootDir"], 'index.html'), 'generated-index.html')

def add_javascript_settings(c):
    shutil.copyfile(os.path.join(c["rootDir"], 'js/prototypes.js'), 'generated-prototypes.js')
    f = open('generated-prototypes.js', 'a')
    f.write('var NATIVE_PLATFORM = "%s";\n' % c["platform"])
    if c["campaignDebug"]:
        f.write('var DEBUG_CAMPAIGN = true;')
    else:
        f.write('var DEBUG_CAMPAIGN = false;')

def get_icons_by_country_id(c, id):
    imgset = set()
    count = 0
    f = os.path.join(c["rootDir"], "resources/equipment", "equipment-country-" + str(id) + ".json")
    with open(f) as jsonfile:
	#print "Building list of unit images for country id %d" % id
	jsondata = json.load(jsonfile)["units"]
	for u in jsondata:
	    imgset.add(jsondata[u][1]) # The index of unit image filename in unit attributes array (only works for condensed equipment per country
	    count += 1
	print "Country %d:  %d unit images which %d are unique" % (id, count, len(imgset))
    return imgset


def get_scenario_icons(c, scenarioFile, alreadyParsedList):
    unitimgset = set()

    if alreadyParsedList is None:
	alreadyParsedList = []

    # Detect the countries id in scenario and their supporting countries
    playerList = etree.parse(scenarioFile).getroot().findall(".//player[@id]")
    for pidx in range(len(playerList)):
	cid = int(playerList[pidx].attrib["country"])
	cid = cid + 1 # IDs of main countries are wrongly offseted by 1
        if cid not in alreadyParsedList and cid > -1:
	    unitimgset = unitimgset.union(get_icons_by_country_id(c, cid))
	    alreadyParsedList.append(cid)
	# supporting countries unique set
	s = set([int(n) for n in playerList[pidx].attrib["support"].split(",")])
	for sid in s:
	    if sid not in alreadyParsedList and sid  > -1:
		unitimgset = unitimgset.union(get_icons_by_country_id(c, sid)) # For supporting countries list ID is correctly saved in scenarios
		alreadyParsedList.append(sid)
    return unitimgset


def generate_game_content(c, filelist):
    # Parse selected campaigns and extract it's scenarios and maps
    f = open(c["campaignFile"])
    cf = open("generated-campaignlist.js", "w")

    # save comment and var declaration without adding bracket which will be saved by json.dump
    cf.write(f.readline() + f.readline().replace('[',''))

    jsondata = "[" # add back the [ that we removed in the first line

    for line in f:
        jsondata += line

    f.close()

    campaignsdata = json.loads(jsondata)
    scenset = set() # set for scenarios
    mapset = set() # set for scenario map images
    unitimgset = set() # set for unit images for all scenarios
    unitimgsetparsed = [] # already searched country ids for unit images

    # Add default selected scenarios and their maps
    for scen in c["selectedScenarios"]:
        scenset.add(scen)
        mapset.add(etree.parse(c["scenarioData"] + scen).getroot().attrib["image"])
	unitimgset = unitimgset.union(get_scenario_icons(c, c["scenarioData"] + scen, unitimgsetparsed))

    # get the list of scenarios from selected campaigns and remove unselected campaigns
    i = 0
    removelist = []
    for cam in campaignsdata:
        if c["selectedCampaigns"] and cam["file"] not in c["selectedCampaigns"]:
            removelist.append(i)  # save index for removal
            continue
        print "Processing %s ... " % cam["file"]
        f = open(os.path.join(c["campaignData"], cam["file"]))
        jsondata = f.read()
        f.close()
        camdata = json.loads(jsondata)
        for scen in camdata:
            #print "\t Found scenario %s " % scen["scenario"]
            scenset.add(scen["scenario"])
            mapset.add(etree.parse(c["scenarioData"] + scen["scenario"]).getroot().attrib["image"])
	    unitimgset = unitimgset.union(get_scenario_icons(c, c["scenarioData"] + scen["scenario"], unitimgsetparsed))

        i += 1
    # remove unlisted campaigns and save a new campaignlist.js
    for i in removelist:
        del campaignsdata[i]

    cf.write(json.dumps(campaignsdata, sort_keys=True, indent=1))
    cf.close()

    # Redo scenariolist.js which isn't a valid json because the use of single quotes
    f = open(c["scenarioFile"])
    sf = open("generated-scenariolist.js", "w")
    for line in f:
        # leave comments and var names untouched
        if not line.startswith('["'):
            sf.write(line)
            continue
        scendesc = line.split(',')
	if len(scendesc) == 2: # Scenario Campaign/Category Marker
	    sf.write(line)
	    print "Found campaign marker %s" % line
	    continue
        scenname = scendesc[0].translate(None, '[]"')
        if scenname in scenset:
            print "Adding scenario %s " % scenname
            sf.write(line)
    sf.close()
    # Add to file list the campaigns, scenarios and maps
    for c in campaignsdata:
        filelist.append("resources/campaigns/data/" + c["file"])
    for s in scenset:
        filelist.append("resources/scenarios/data/" + s)
    for m in mapset:
        filelist.append(m) # this already has full path
    for u in unitimgset:
	filelist.append(u) # this already has full path


def generate_initial_filelist(c, filelist):
    for p in [os.path.join(c["rootDir"], inclpath) for inclpath in c["includeFiles"]]:
        if os.path.isfile(p):
            filelist.append(p.replace(c["rootDir"], ""))
            continue
        for root, dirs, files in os.walk(p, topdown=True):
            for d in dirs:
                path = os.path.join(root, d).replace(c["rootDir"], "")
                for excl in c["excludeFiles"]:
                    if path.startswith(excl) or d == excl:
                        print "Removing path %s" % path
                        dirs.remove(d)
            for f in files:
                absfile = os.path.join(root,f).replace(c["rootDir"], "")
                filtered = 0
                for excl in c["excludeFiles"]:
                    if fnmatch.fnmatch(absfile, excl) or f == excl:
                        filtered = 1
                        break
                if not filtered:
                    filelist.append(absfile)
