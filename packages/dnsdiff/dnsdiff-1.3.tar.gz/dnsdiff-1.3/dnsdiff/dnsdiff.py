'''Module to quickly look up and compare NS records for differences'''

import dns.resolver
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def compare_dns(nameservers, domain):
	'''Compares records between nameservers using dnspython'''

	responses = {}
	resolver = dns.resolver.Resolver(configure=False)

	for ns in nameservers:
		ns_list = []
		resolver.nameservers = ns
		answer = dns.resolver.query(domain, 'NS')
		for record in answer:
			ns_list.append(record.target)
		responses[ns] = sorted(ns_list)

	pp.pprint(responses)
	print "Determining differences"

	set_list = []
	for val in responses.values():
		set_list.append(set(val))

	differences = set.difference(*set_list)

	if len(differences) == 0 or len(nameservers) == 1:
		print "No discrepancies found"
		sys.exit(0)
	else:
		print "Discrepancies found!"
		print differences
		sys.exit(1)
