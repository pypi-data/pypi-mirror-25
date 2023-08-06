# -*- encoding: utf8 -*-
# © Toons

from .. import __PY3__, __FROZEN__, ROOT, api, cfg

import os, io, sys, json

def ceilContribution(contribution, ceil):
	cumul = 0
	# first filter
	for address,force in [(a,f) for a,f in contribution.items() if f >= ceil]:
		contribution[address] = ceil
		cumul += force - ceil
	# report cutted share
	untouched_pairs = sorted([(a,f) for a,f in contribution.items() if f < ceil], key=lambda e:e[-1], reverse=True)
	n, i = len(untouched_pairs), 0
	bounty = cumul / max(1, n)
	for address,force in untouched_pairs:
		if force + bounty > ceil:
			i += 1
			n -= 1
			contribution[address] = ceil
			bounty = (cumul - abs(ceil - force)) / max(1, n)
		else:
			break
	for address,force in untouched_pairs[i:]:
		contribution[address] += bounty

	return contribution

def normContribution(contribution):
	k = 1.0/max(1, sum(contribution.values()))
	return dict((a, s*k) for a,s in contribution.items())
