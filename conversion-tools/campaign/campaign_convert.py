#!/usr/bin/python
#Copyright 2012 Nicu Pavel <npavel@linuxconsulting.ro>
#Licensed under GPLv2

# Exports a Panzer General 2 campaign file (.CAM) to JSON format
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
from struct import *
from config.config import *


# the list of dictionaries that holds information for all campaigns converted
campaign_list = []

# destpath for campaigns
destpath = os.path.join(DESTPATH, "campaigns")

def create_destpath():
	if not os.path.exists(destpath):
		os.makedirs(destpath)
		os.makedirs(os.path.join(destpath, 'data'))

def filename_case(name):
    if not PRESERVE_CASE:
	return name.lower()
    return name

def parse_info(folder, f):
	info = {}
	info['title'] = "No title"
	info['desc'] = "No description"
	
	pos = f.tell()
	f.seek(0)
	data = f.read(4)
	info['scenarios'] = unpack('h', data[0:2])[0]
	info['prestige'] = unpack('h', data[2:4])[0]
	f.seek(f.tell() + 20 + 20 + 50 * 636)
	data = f.read(20)
	txtfile = data.strip('\0').lower()
	f.seek(f.tell() + 78)
	data = f.read(1)
	info['flag'] = unpack('b',data[0:1])[0] - 1 #TODO Fix this, bad country indexes was carried from a badly installation of pg2
	with open(os.path.join(folder, txtfile), 'r') as txt:
		lines = txt.readlines()
		info['title'] = lines[0].title().replace("\r\n", "")
		info['desc'] = "".join(lines[2:]).replace("\r\n\r\n","<br>")
		txt.close()
	
	f.seek(pos)
	return info

def parse_scenario(folder, f, i):
	scenario = {}
	scenario['outcome'] = {} #hash for victory types (briliant, normal, tactical) or lose
	outcome = {} #outcome hash lists prestige and text for outcome
	scenario['id'] = i;
	scenario['intro'] = "No intro"
	pos = f.tell()
	f.seek(2 + 2 + 20 + 20 + i * 636) #jump to the beginning of scenario information
	data = f.read(636)
	scenario['startprestige'] = unpack('h', data[6:8])[0]
	#also strip scn extension and replace with .xml
	scenario['scenario'] = data[8:28].lower().strip('\0').split('.')[0] + ".xml"
	introfile = filename_case(data[68:88].strip('\0'))
	try:
		intro = open(os.path.join(folder, introfile), 'r')
	except IOError:
		try:
			intro = open(os.path.join(folder, introfile + '.txt'), 'r')
		except IOError:
		    print "\tWarning: No intro file (readed from %s in scenario %s)." % (introfile, scenario['scenario'])

	try:
		scenario['intro'] = ''.join(intro.readlines())
		scenario['intro'] = format_text(scenario['intro'])
		intro.close()
	except:
		pass

	pdata = 88 # start pointer in data list
	goto_chunk = 4 #where to jump to get scenario goto information
	#build outcome prestige gains and text for each type
	for o in ['briliant', 'victory', 'tactical', 'lose']:
		outcome['prestige'] = unpack('h', data[pdata:pdata + 2])[0]
		pdata += 2; #move to the end of the read section
		pdata += 40; #skip SMK and MUS
		textfile = filename_case(data[pdata:pdata + 20].strip('\0'))
		try:
			text = open(os.path.join(folder, textfile), 'r')
		except IOError:
			try:
				text = open(os.path.join(folder, textfile + '.txt'), 'r')
			except IOError:
				print "\tWarning: No outcome text for %s in scenario %d" % (o, i)

		try:
			outcome['text'] = ''.join(text.readlines())
			outcome['text'] = format_text(outcome['text'])
			text.close()
		except:
			pass

		pdata+= 20; #move to the end of the read section
		pdata+= 20; #skip SMK after TXT
		goto_pos = 636 - 100 - (24 + 6) * goto_chunk
		#to which scenario to jump in this outcome
		outcome['goto'] = unpack('h', data[goto_pos:goto_pos + 2])[0]
		#or jump to
		played_goto = [0, 0] #if scenario [0] has been played goto [1]
		played_goto[0] = unpack('h', data[goto_pos + 2:goto_pos + 4])[0]
		played_goto[1] = unpack('h', data[goto_pos + 4:goto_pos + 6])[0]
		outcome['gotoplayed'] = played_goto
		goto_chunk = goto_chunk - 1
		scenario['outcome'][o] = outcome.copy()
		
	f.seek(pos);
	return scenario

# Parses and extracts info from a .cam file
def parse_campaign_file(file, output_list):
	folder, campaign = os.path.split(file)
	if folder == '':
		folder ='./'
	else:
		folder += '/'

	try:
		cam = open(os.path.join(folder, campaign), 'r')
	except IOError:
		print "Can't open file %s" % campaign
		return;

	print "Working in %s" % folder
	print "Processing %s" % campaign
	info = parse_info(folder, cam)
	info['file'] = os.path.splitext(campaign)[0].lower() + ".json";
	campaign_list.append(info.copy())
	# the list of all scenarios in a campaign
	scenario_list = []
	for i in range(info['scenarios']):
		scenario = parse_scenario(folder, cam, i)
		scenario_list.append(scenario.copy())
		scenario_file_name = scenario['scenario'].split('.')[0] + '.scn'
		scenario_intro_text = scenario['intro']
		output_list.append({
		    'scenario': scenario_file_name,
			'path': folder,
		    'intro': scenario_intro_text
		    })
	camdata = open(os.path.join(destpath, 'data', info['file']), 'w')
	out = json.dumps(scenario_list, sort_keys=True, indent=1)
	camdata.write(out)
	camdata.close()

def format_text(desc, utf_decode=True):
	if utf_decode:
	    desc = desc.decode('utf-8', 'ignore')
	nstr = desc.replace("\r\n\r\n","<br><br>").replace("\r\n","<br>").replace("\n", "").replace("\r", "")
	return nstr.replace('"', '\"')

# Generates the index .js file with all converted campaigns
def generate_campaigns_list():
	print "Generating campaign index"
	camlist = open(os.path.join(destpath, 'campaignlist.js'), 'w')
	out = json.dumps(campaign_list, sort_keys=True, indent=1)
	camlist.write('//Automatically generated by campaing-convert.py\n')
	camlist.write('var campaignlist = ');
	camlist.write(out)
	camlist.close()

if __name__ == "__main__":
	scn_scenario_list = [] # will hold the list of scn scenarios that need to be converted
	cam_list = [] # will hold the list of campaign files that need to be processed
	create_destpath()

	print "Assets path: %s" % PG2_ASSETS_PATH

	for cam in KNOWN_CAMPAIGNS: # preserves the list order in output
		for root, dirs, files in os.walk(os.path.join(PG2_ASSETS_PATH, 'campaigns')):
			if cam in files:
				cam_list.append(os.path.join(root, cam))

	for file in cam_list:
		parse_campaign_file(file, scn_scenario_list)

	generate_campaigns_list()

	#pprint(scn_scenario_list)

	# Add the non campaign scenarios
	scn_scenario_list.append({
	    'scenario':'tutorial.scn',
		'path': os.path.join(PG2_ASSETS_PATH, 'campaigns', 'eqp-adlerkorps', 'TUTORIAL_CAM'),
	    'intro': None}
	)

	if SCENARIO_CONVERT:
		sys.path.append('../scenario/')
		import scenario_convert

		converter = scenario_convert.MapConvert()
		for scn in scn_scenario_list:
			scnfile = os.path.join(scn['path'], scn['scenario'])
			converter.parse_scenario_file(scnfile, scn['intro'])
		converter.generate_scn_js_file()

		print "Maps to copy to openpanzer installation: "
		for m in converter.maplist:
			print "%s " % m,
		
	else:
		print "Scenarios to convert with mapconvert.py: "
		for scn in scn_scenario_list:
			print  "%s " % scn,
