import requests
import json

# Usage: python flush-nodes.py | tail | /usr/bin/xargs -I % curl -X PUT -d'%' http://localhost:8500/v1/catalog/deregister

nodes = requests.get("http://localhost:8500/v1/health/service/discussion")
for node in nodes.json():
    for check in node['Checks']:
        if check['Status'] == 'critical':
            payload = {"ServiceID": check['ServiceID'], "Node": check['Node']}
            #print json.dumps(payload)

            print "'{\"ServiceID\": \"%s\", \"Node\": \"%s\"}'" % (check['ServiceID'], check['Node'])

