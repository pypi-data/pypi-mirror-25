# -*- encoding: utf8 -*-
# © Toons

'''
Usage: network use [<name>]
       network browse [<element>]
       network publickey <secret>
       network address <secret>
       network delegates

Subcommands:
    use       : select network.
    browse    : browse network.
    publickey : returns public key from secret.
    address   : returns address from secret.
    delegates : show delegate list.
'''

from .. import cfg, api, util, crypto

import sys, hashlib, webbrowser

def _whereami():
	return "network"

def use(param):
	if not param["<name>"]:
		choices = util.findNetworks()
		if choices:
			param["<name>"] = util.chooseItem("Network(s) found:", *choices)
		else:
			sys.stdout.write("No Network found\n")
			return False
	api.use(param["<name>"])

def browse(param):
	element = param["<element>"]
	if element:
		if element.endswith("X"):
			webbrowser.open(cfg.explorer + "/address/" + element)
		elif element == "delegate":
			webbrowser.open(cfg.explorer + "/delegateMonitor")
		else:
			webbrowser.open(cfg.explorer + "/tx/" + element)
	else:
		webbrowser.open(cfg.explorer)

def address(param):
	sys.stdout.write("    %s\n" % crypto.getAddress(crypto.getKeys(param["<secret>"].encode("ascii"))[0]))

def publickey(param):
	sys.stdout.write("    %s\n" % crypto.getKeys(param["<secret>"].encode("ascii"))[0])

def delegates(param):
	delegates = api.GET.delegates(limit=cfg.delegate, returnKey='delegates')
	maxlen = max([len(d["username"]) for d in delegates])
	i = 1
	for name, vote in sorted([(d["username"],float(d["vote"])/100000000) for d in delegates], key=lambda e:e[-1], reverse=True):
		sys.stdout.write("    #%03d - %s: %.3f\n" % (i, name.ljust(maxlen), vote))
		i += 1
