__author__ = 'panic'
#!/usr/bin/env python
import urllib
import urllib2
import json
import sys, os
from datetime import datetime, timedelta

site = 'https://api.github.com'
token = ''
download_dir = "downloaded"
gist_cache = "all-gists.json"
gist_file = "openpanzer-save.json" # the name of the file with content from the gist

def get_gists():
    headers = {}

    headers['Accept'] = 'application/vnd.github.raw'
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'bearer ' + token

    page = 0
    older = 0
    now = datetime.now()

    gists = []

    while True:
        request = urllib2.Request(site + "/gists?per_page=100&page=" + str(page), headers=headers)
        reply = urllib2.urlopen(request)

        gistsdata = json.loads(reply.read())
        if len(gistsdata) == 0:
            break

        for g in gistsdata:
            id = str(g['id']) # Doesn't have unicode characters
            #2014-05-10T07:29:30Z
            last_update_date = datetime.strptime(g['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            gists.append(id)

        print "Page %d : %d results" % (page, len(gistsdata))
        page += 1

    return gists

def download_gists(gists):

    try:
        os.mkdir(download_dir)
    except Exception:
        pass

    try:
        os.chdir(download_dir)
    except Exception, e:
        print("Cannot chdir to %s aborting !" % download_dir)
        return False

    downloaded = 0
    errors = 0
    headers = {}

    headers['Accept'] = 'application/vnd.github.raw'
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'bearer ' + token

    for id in gists:
        filename = id + ".json"
        if os.path.isfile(filename):
            print "Skipping file %s already exists " % filename
            continue

        print "Downloading %s" % filename
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            url =  site + "/gists/" + id
            request = urllib2.Request(url, headers=headers)
            request.get_method = lambda: 'GET'
            reply = opener.open(request)
            gist = json.loads(reply.read())
        except Exception, e:
            print "Can't download %s" % id
            errors += 1

        try:
            content = gist['files'][gist_file]['content']
            with open(filename, "w") as f:
                f.write(content)
            downloaded += 1
        except Exception, e:
            print "Invalid content for file %s" % filename
            errors += 1
            continue

    print "Downloaded %d Errors %d" % (downloaded, errors)
    return True

def main():

    gists = []
    should_download = False
    try:
        with open(gist_cache, 'r') as fp:
            gists = json.load(fp)
        print "Found cached gist list with %d entries" % len(gists)
    except Exception:
        print "Cannot find saved gists information downloading gists..."
        should_download = True

    if should_download:
        gists = get_gists()
        with open(gist_cache, 'w') as fp:
            print "Saving %d retrieved gists " % len(gists)
            json.dump(gists, fp)

    download_gists(gists)

if __name__ == '__main__':
    main()
