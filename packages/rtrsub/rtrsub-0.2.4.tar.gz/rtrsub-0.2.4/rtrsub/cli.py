#!/usr/bin/env python
# rtrsub - A RTR Substitution
#
# Copyright (C) 2016 Job Snijders <job@instituut.net>
#
# This file is part of rtrsub
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function

from collections import OrderedDict
from ipaddress import ip_network
from operator import itemgetter
import jinja2
import json
import pprint
import os
import sys

try:
    import argparse
except ImportError:
    print("ERROR: install argparse manually")
    print("HINT: sudo pip install argparse")
    sys.exit(2)

try:
    import requests
except ImportError:
    print("ERROR: requests missing")
    print("HINT: pip install requests")
    sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', dest='cache',
                        default="http://localcert.ripe.net:8088/export.json",
                        type=str,
                        help="""Location of the RPKI Cache in JSON format
(default: http://localcert.ripe.net:8088/export.json)""")

    parser.add_argument('--afi', dest='afi', type=str, required=True,
                        help="[ ipv4 | ipv6 | mixed ]")

    parser.add_argument('-t', dest='template', type=str,
                        default="-", help='Template file (default: STDIN)')

    parser.add_argument('-o', dest='output', type=str,
                        default='-',
                        help='Output file (default: STDOUT)')

    parser.add_argument('-v', dest='version', action='store_true',
                        help="Display rtrsub version")

    parser.add_argument('-r', dest='ruby', action='store_true',
                        help='Use other delimiters')

    args = parser.parse_args()

    if args.afi not in ["ipv4", "ipv6", "mixed"]:
        print("ERROR: afi must be 'ipv4', 'ipv6' or 'mixed'")
        sys.exit(2)

    if args.ruby:
        env = jinja2.Environment(
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<%=',
            variable_end_string='%>',
            comment_start_string='<#',
            comment_end_string='#>',
            line_statement_prefix="%%")
    else:
        env = jinja2.Environment()

    if args.template == "-":
        template_stdin = sys.stdin.read()
        template = env.from_string(template_stdin)
    else:
        template = env.from_string(open(os.path.abspath(args.template), 'r').read())

    if 'http' in args.cache:
        r = requests.get(args.cache)
        validator_export = r.json()
    else:
        validator_export = json.load(open(args.cache, "r"))

    data = load_pfx_dict(args.afi, validator_export)
    data['afi'] = args.afi

    if args.output == "-":
        print(template.render(**data))
    else:
        f = open(args.output, 'w')
        f.write(template.render(data=data))
        f.close


def load_pfx_dict(afi, export):
    """
    :param afi:     which address family to filter for
    :param export:  the JSON blob with all ROAs
    """
    pfx_dict = {}
    origin_dict = {}
    pfx_list = []

    """ each roa has these fields:
        asn, prefix, maxLength, ta
    """

    for roa in export['roas']:
        prefix_obj = ip_network(roa['prefix'])
        if afi == "ipv4":
            if prefix_obj.version == 6:
                continue
        elif afi == "ipv6":
            if prefix_obj.version == 4:
                continue

        try:
            asn = int(roa['asn'].replace("AS", ""))
            if not 0 <= asn < 4294967296:
                raise ValueError
        except ValueError:
            print("ERROR: ASN malformed", file=sys.stderr)
            print(pprint.pformat(roa, indent=4), file=sys.stderr)
            continue

        prefix = str(prefix_obj)
        prefixlen = prefix_obj.prefixlen
        maxlength = int(roa['maxLength'])

        if prefix not in pfx_dict:
            pfx_dict[prefix] = {}
            pfx_dict[prefix]['origins'] = [asn]
        else:
            if asn not in pfx_dict[prefix]['origins']:
                pfx_dict[prefix]['origins'] += [asn]

        pfx_dict[prefix]['maxlength'] = maxlength
        pfx_dict[prefix]['prefixlen'] = prefixlen
        pfx_list.append((prefix, prefixlen))

        if asn not in origin_dict:
            origin_dict[asn] = {}

        origin_dict[asn][prefix] = {'maxlength': maxlength,
                                    'length': prefixlen}

    # order the list of prefixes by prefix length
    pfx_list = map(lambda x: x[0], sorted(pfx_list, key=itemgetter(1)))
    # deduplicate the list and maintain the order
    pfx_list = list(OrderedDict.fromkeys(pfx_list))

    return {"pfx_dict": pfx_dict, "origin_dict": origin_dict,
            "pfx_list": pfx_list}

if __name__ == '__main__':
    main()
