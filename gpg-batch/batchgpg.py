#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## (cc) 2015 Luis Rodil-Fernandez <root@derfunke.net>
## Generate labels from revocation certificates and manage printing queue
##
##
CLII = """
Tool for gnupg key management used in the key2myheart installation.

Usage:
  keypipe generate --name=<name> --email=<email>
  keypipe revocation [--keyid=<keyid>]
  keypipe shred
  keypipe -h | --help

Commands:
  generate              Generate keypair for given name and email address.
  revocation            Get revocation certificate for requested key id.
  shred                 Digitally shred all generated keys and certificates.

Options:
  -h --help             Show this screen.
  --name=<name>         Name of key's owner.
  --email=<email>       Email address of key's owner.
  --keyid=<keyid>       Id of key to generate certificate for.
"""
import sys, os
import json
import re
import pipes
from subprocess import Popen, PIPE
import shutil, time
from docopt import docopt
import gnupg
import subprocess
import pexpect

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
%commit
%echo Key generated. Done.
"""

KEYRING_DIR="./temp.gnupg"

gpg = gnupg.GPG(homedir=KEYRING_DIR)

def default_spec():
	return KEYSPEC.format(type='RSA', 
							length=4096, 
							subtype='ELG-E', 
							sublength=4096, 
							name='Kermit van Frog', 
							comment='', 
							email='kermit@invalid.tld', 
							expire='0', 
							pubring='foo.pub', 
							secring='foo.sec')

def generate_spec(params):
	return KEYSPEC.format(type=params["type"], 
							length=params["length"], 
							subtype=params["subtype"], 
							sublength=params["sublength"], 
							name=params["name_real"], 
							comment=params["comment"], 
							email=params["name_email"], 
							expire=params["expire"])

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
	""" make sure username is a valid string """
	return re.match("^[a-zA-Z0-9]+$", uname)


def shred_keyring(pubkring, seckring):
	""" shred the keyring files """
	for f in (pubkring, seckring):
		os.system("shred -n 10 -u -z -v {0}".format(f))

def generate_keys(cfgarr):
	""" Generate GPG keys using a dynamically generated parameter file. For this purpose
	we use gpg in batch mode: gpg --batch --gen-key
	see man page for further details: https://www.gnupg.org/documentation/manpage.html
	"""
	spec = generate_spec(cfgarr)
	begin = time.time()
	retkey = gpg.gen_key(spec)
	end = time.time()
	from pprint import pprint
	pprint(retkey)
	print "generated key with fp: ", retkey.fingerprint, "and keyid", "in", (end-begin), "seconds"

	pubkey = gpg.export_keys(retkey.fingerprint)
	seckey = gpg.export_keys(retkey.fingerprint, secret=True)

	print "exported pubkey: ", pubkey

	return retkey
	# p = os.popen("gpg --batch --gen-key ", 'w')
	# p.write(spec)
	# #print spec
	# p.close()

def get_generated_key(params):
	""" get key id and fingerprint of generated key """
	os.popen("gpg --primary-keyring {0} --list-keys --no-default-keyring --homedir .".format(params["pubring"]) )

def get_revocation_certificate(keyid):
	print "Using keyring", KEYRING_DIR
	cmd = "gpg --homedir {0} --gen-revoke {1}".format(KEYRING_DIR, keyid)
	print "Command: ", cmd
	px = pexpect.spawn(cmd, timeout=5)

	px.expect("(y/N)")
	px.sendline("y")
	px.expect("Your decision?")
	px.sendline('0')
	px.expect("> ")
	px.sendline("\n")
	px.sendline("\n")
	px.expect("Is this okay?")
	px.sendline("y")

	px.expect(pexpect.EOF)

	# print "before: ", px.before
	# print "buffer: ", px.buffer
	# print "after: ", px.after

	bidx = px.before.index('-----BEGIN PGP PUBLIC KEY BLOCK-----')
	eidx = px.before.index('-----END PGP PUBLIC KEY BLOCK-----')
	eidx += len('-----END PGP PUBLIC KEY BLOCK-----')
	print "## certificate"
	print px.before[bidx:eidx]


def main():
	cfg = read_stdin()

	# check and validate input values
	# check_input(cfg, 'username')
	# if not validate_username(cfg['username']):
	# 	print "Illegal username"
	# 	sys.exit(1)

	# get username from config object
	#username = cfg['username']
	generate_keys(cfg)


if __name__ == "__main__":
	main()