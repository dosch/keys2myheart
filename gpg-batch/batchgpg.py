#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import json
import re
import pipes
from subprocess import Popen, PIPE

KEYSPEC = """
%echo Generating an OpenPGP key
Key-Type: {type}
Key-Length: {length}
Subkey-Type: {subtype}
Subkey-Length: {sublength}
Name-Real: {name}
Name-Comment: {comment}
Name-Email: {email}
Expire-Date: {expire}
Passphrase: {passphrase}
%pubring {pubring}
%secring {secring}
%commit
%echo Key generated. Done.
"""

def default_spec():
	return KEYSPEC.format(type='RSA', 
							length=4096, 
							subtype='ELG-E', 
							sublength=4096, 
							name='Kermit van Frog', 
							comment='', 
							email='kermit@invalid.tld', 
							expire='0', 
							passphrase='badpassphrase', 
							pubring='foo.pub', 
							secring='foo.sec')

def generate_spec(params):
	return KEYSPEC.format(type=params["type"], 
							length=params["length"], 
							subtype=params["subtype"], 
							sublength=params["sublength"], 
							name=params["name"], 
							comment=params["comment"], 
							email=params["email"], 
							expire=params["expire"], 
							passphrase=params["passphrase"], 
							pubring=params["pubring"], 
							secring=params["secring"])

def read_stdin():
	""" Read configuration from standard input, expects JSON string """
	istr = ''
	# Read data from STDIN, expect json input
	for line in sys.stdin:
		istr = istr + line

	print istr
	return json.loads(istr)

def check_input(cfgarr, param):
	try:
		cfgarr[param]
	except KeyError as i:
		print "Parameter '{0}' not defined in stdin configuration".format(param)
		sys.exit(1)


def validate_username(uname):
	return re.match("^[a-zA-Z0-9]+$", uname)


def generate_keys(cfgarr):
	""" Generate GPG keys using a dynamically generated parameter file. For this purpose
	we use gpg in batch mode: gpg --batch --gen-key
	see man page for further details: https://www.gnupg.org/documentation/manpage.html
	"""
	spec = generate_spec(cfgarr)
	p = os.popen('gpg --batch --gen-key', 'w')
	p.write(spec)
	#print spec
	p.close()

def main():
	cfg = read_stdin()

	# check and validate input values
	check_input(cfg, 'username')
	if not validate_username(cfg['username']):
		print "Illegal username"
		sys.exit(1)

	# get username from config object
	username = cfg['username']
	generate_keys(cfg)


if __name__ == "__main__":
    main()
