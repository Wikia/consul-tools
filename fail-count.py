from optparse import OptionParser
import requests
import json
import time
import sys

def get_checks(url):
    response = requests.get(url)
    nodes = [node for node in response.json()]
    check_blocks = [node['Checks'] for node in nodes]
    checks = [check for sublist in check_blocks for check in sublist]
    return [check for check in checks if check['CheckID'] != "serfHealth"]


def filter_checks_by_status(checks, status):
    return [check for check in checks if check['Status'] == status]

def print_node(message, node):
    print "\t{0}:{1} {2}".format(message, node['Node'], node['ServiceID'])

if __name__ == '__main__':
    usage = """usage: %prog [options]
        """
    parser = OptionParser(usage)
    parser.add_option("-H", "--consul-host", dest="consul_host", \
            help="consul host to connect to")
    parser.add_option("-s", "--service", dest="service", help="service to query")
    parser.add_option("-P", "--no-passing", dest="passing", default=True, \
            action="store_false", help="don't show passing services")
    parser.add_option("-F", "--no-failed", dest="failed", default=True, \
            action="store_false", help="don't show failed services")

    (options, args) = parser.parse_args()

    if options.consul_host and options.service:
        health_url = "http://{0}:8500/v1/health/service/{1}".format(options.consul_host, options.service)
    else:
        parser.error("-H and -s are required")

    print "Querying {0}...".format(health_url)
    time.sleep(1)


    while True:
        checks = get_checks(health_url)
        failing = filter_checks_by_status(checks, "critical")
        passing = filter_checks_by_status(checks, "passing")

        print "{0}\t{1}".format(time.strftime('%X %x %Z'), len(failing))
        if options.failed:
            for failed in failing: print_node("failed", failed)
        if options.passing:
            for passed in passing: print_node("healthy", passed)
        time.sleep(2)
