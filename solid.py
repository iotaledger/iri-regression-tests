import json
import urllib2
import sys
from sets import Set

import time

url = "http://localhost:" + sys.argv[1]
folder = './'


#Utils:
all_nines = '9' * 81
TIMEOUT = 7
def API(request,url=url):

    stringified = json.dumps(request)
    headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}

    try:
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        returnData = urllib2.urlopen(request,timeout=TIMEOUT).read()
        response = json.loads(returnData)

    except:
        print url, "Timeout!"
        print '\n    ' + repr(sys.exc_info())
        return ""
    if not response:
        response = ""
    return response

def getNodeInfo():
    cmd = {
        "command": "getNodeInfo"
    }
    return API(cmd)

def getTrytes(hash):
    cmd = {
        "command": "getTrytes",
        "hashes" : [hash]
    }
    return API(cmd)



# check that node is solid:
# and get latest milestone hash
solid_milestone = False
counter = 0
while not solid_milestone:
    node_info = getNodeInfo()
    if node_info != "":
        if node_info['latestSolidSubtangleMilestone'] != all_nines:
            if node_info['latestSolidSubtangleMilestoneIndex'] == node_info['latestMilestoneIndex']:
                solid_milestone = node_info['latestSolidSubtangleMilestone']
                print "Success! node solid - solid_milestone: " + solid_milestone
                break
        print "waiting for node to get solid:" + str(node_info['latestSolidSubtangleMilestoneIndex']) + "/" + str(node_info['latestMilestoneIndex'])
        time.sleep(2)
        counter += 1
        if counter > 30:
            print "Error! not becoming solid!"
    else:
        print "waiting for API"
        time.sleep(10)