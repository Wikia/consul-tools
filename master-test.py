import requests
import time

def count_healthy(uri):
    services = requests.get(uri)
    return len(services.json())

s = requests.get("http://dev-consul.wikia.prod:8500/v1/health/service/discussion?passing")
print s.json()

#while True:
#    print "pass"
#    print "{0} {1}\n".format("http://dev-consul-s1.wikia.prod:8500/v1/health/service/discussion?passing", count_healthy("http://dev-consul-s1.wikia.prod:8500/v1/health/service/discussion?passing"))
#    #print "{0} {1}\n".format("http://dev-consul.wikia.prod:8500/v1/health/service/discussion?passing", count_healthy("http://dev-consul.wikia.prod:8500/v1/health/service/discussion?passing"))
#    #print "{0} {1}\n".format("http://dev-broker.wikia.prod:8500/v1/health/service/discussion?passing", count_healthy("http://dev-broker.wikia.prod:8500/v1/health/service/discussion?passing"))

