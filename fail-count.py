import argparse
import requests
import json
import time
import sys
import consul

def get_checks(consul_client, service):
    index, nodes = consul_client.health.service(service)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--consul-host", dest="consul_host", \
            help="consul host to connect to")
    parser.add_argument("-s", "--service", dest="service", help="service to query")
    parser.add_argument("-P", "--no-passing", dest="passing", default=True, \
            action="store_false", help="don't show passing services")
    parser.add_argument("-F", "--no-failed", dest="failed", default=True, \
            action="store_false", help="don't show failed services")

    options = parser.parse_args()

    if options.consul_host and options.service:
        consul_client = consul.Consul(options.consul_host)
    else:
        parser.error("-H and -s are required")

    print "Querying {0}...".format(options.consul_host)
    time.sleep(1)


    while True:
        checks = get_checks(consul_client, options.service)
        failing = filter_checks_by_status(checks, "critical")
        passing = filter_checks_by_status(checks, "passing")

        print "{0}\t{1}".format(time.strftime('%X %x %Z'), len(failing))
        if options.failed:
            for failed in failing: print_node("failed", failed)
        if options.passing:
            for passed in passing: print_node("healthy", passed)
        time.sleep(2)
