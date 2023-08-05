#!/usr/bin/env python

import argparse
from . import firewall_filter
from pyparsing import *
import sys
import ipaddress

class ACLSearch(object):

    def __init__(self):
        self.term_dict = {}
        self.ip_dict = {}

        if not sys.version_info < (3,):
            print("This tool is not compatible with Python 3")
            sys.exit(-1)

        args = self._accept_cli_args()

        self.ip_addr = ipaddress.ip_network(args['ip'])
        acl_file = args['acl_file']
        print("Reading Firewall File and Building Structure to Search..")
        self.acl_str = acl_file.read()
        self.ff = firewall_filter.FirewallFilter()

        self._create_term_and_ip_dicts()
        print("Finished Initing.")



    def _accept_cli_args(self):
        arg_parser = argparse.ArgumentParser(description='Searches for an IP or intersecting CIDR in the destination block within an ACL file and returns the full term.')
        arg_parser.add_argument('ip', type=bytearray, help="an IP address to search for")
        arg_parser.add_argument('acl_file', type=argparse.FileType('r'), help='path to the ACL file to search in')

        args = arg_parser.parse_args()

        if "/" not in args.ip:
            args.ip = args.ip + '/32'

        return vars(args)

    def _create_term_and_ip_dicts(self):
        for term in self.ff.firewall_filter_term_original().scanString(self.acl_str):
            self.term_dict[self.ff.firewall_filter_term_key().scanString(term[0][0]).next()[0][0]] = term[0][0]

        for key, term in self.term_dict.items():
            dest_ips = []
            dest_ip_list = []
            try:
                dest_ip_list = self.ff.firewall_filter_dest_addr_block().scanString(term).next()[0][0]
            except:
                None
            for dest_ip in dest_ip_list:
                dest_ips.append(ipaddress.ip_network(bytearray(dest_ip)))
            self.ip_dict[key] = dest_ips

    def search(self):
        print("Searching...")
        results = []
        for term_key, ip_list in self.ip_dict.items():
            for ip in ip_list:
                if ip.overlaps(self.ip_addr):
                    results.append(term_key)
        return set(results)


def main():
    aclSearch = ACLSearch()
    results = aclSearch.search()
    for result in results:
        print(aclSearch.term_dict[result])
    print("#"*100)
    print("FOUND {0} Results!".format(len(results)))
