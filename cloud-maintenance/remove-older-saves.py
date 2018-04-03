#!/usr/bin/env python
import urllib
import urllib2
import json
from datetime import datetime, timedelta

site = 'https://api.github.com'
token = ''
past_days = 2 * 30
max_pages = 100

def get_old_gists():
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
            break;

        for g in gistsdata:
            id = str(g['id']) # Doesn't have unicode characters
            #2014-05-10T07:29:30Z
            last_update_date = datetime.strptime(g['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
	    #print last_update_date
	    delta = now - last_update_date
            if delta.days >= past_days:
                gists.append(id)
                older += 1

        print "Page %d : %d results (%d) older than %d days" % (page, len(gistsdata), older, past_days)
        page += 1
        older = 0
	if page > max_pages:
	    print "Limiting this session to %d pages, retry for more pages"
	    break

    return gists

def remove_gists(gists):

    headers = {}

    headers['Accept'] = 'application/vnd.github.raw'
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'bearer ' + token

    for id in gists:
        print "Removing %s" % id
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            url =  site + "/gists/" + id
            request = urllib2.Request(url, headers=headers)
            request.get_method = lambda: 'DELETE'
            reply = opener.open(request)
        except Exception, e:
            print "Can't delete %s" % id



def main():
    gists = get_old_gists()
    remove_gists(gists)

if __name__ == '__main__':
    main()
