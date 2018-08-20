import api
import time
import sys

bundle_trytes ="GDDDPCAD9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999VCBPMVHSLISYGDCEAYH9PYNCITGQGXMRMMVQSJOR9YTSMIUCDILBWW9GATZDNBCNYXOGLLTNBIMQMO9LW999999999999999999999999999SXAM99999999999999999999999MAUSWYD99999999999999999999FANLKRRSRVOFSLJT9JDIIK9YGLHZZJTRSJFJJXDGLYVELFJIQVIXQQXU9FVVNHIRPLQJJBYQPEDHXYHEB999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999SPAM99999999999999999999999999999999999999999999999999999999999999999999999999999"

port_1 = int(sys.argv[1])
port_2 = port_1 + 1

url1 = "http://localhost:" + `port_1`
url2 = "http://localhost:" + `port_2`

counter = 0
while True:
    node_info1 = api.getNodeInfo(url1)
    node_info2 = api.getNodeInfo(url2)
    if node_info1 != "" and node_info2 != "":
        break
    else:
        print "waiting for API"
        time.sleep(10)
        counter += 1
        if counter > 30:
            print "Error! API not answering!"
            exit(-1)

result = api.attachToTangle(url1, api.all_nines, api.all_nines, 9, bundle_trytes)
if not result:
    print 'attach to tangle failed'
    exit(-1)

bundle_trytes = result.get('trytes')[0]

result = api.storeTransactions(url1, bundle_trytes)

result = api.broadcastTransactions(url1, bundle_trytes)

time.sleep(1)

result = api.findTransactions(url2, "SXAM")
if not result:
    print 'find transactions failed'
    exit(-1)

found_hashes = result.get('hashes')

if (len(found_hashes) == 0):
    print 'Expecting: at least 1 transaction hash' + '\n  Actual: ' + str(found_hashes)
    exit(-1)

print "TEST SUCCESS"
