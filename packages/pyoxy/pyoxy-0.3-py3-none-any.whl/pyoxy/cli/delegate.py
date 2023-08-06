# -*- encoding: utf8 -*-
# © Toons

'''
Usage: delegate link <secret> [<2ndSecret>]
       delegate unlink
       delegate status
       delegate share <amount> [-c -b <blacklist> -d <delay> -l <lowest> -h <highest>]

Options:
-b <blacklist> --blacklist <blacklist> account addresses to exclude (comma-separated list or pathfile)
-h <highest> --highest <hihgest>       maximum payout during payroll
-l <lowest> --lowest <lowest>          minimum payout during payroll
-d <delay> --delay <delay>             number of fidelity-day [default: 30]
-c --complement                        share the amount complement

Subcommands:
    link     : link to account using secret passphrases. If secret passphrases
               contains spaces, it must be enclosed within double quotes
               ("secret with spaces").
    unlink   : unlink account.
    status   : show information about linked account.
    share    : send OXY amount to address.
'''

from .. import cfg, api, util, crypto
from . import share as _share

import io, os, sys, collections

ADDRESS = None
PUBLICKEY = None
PRIVKEY1 = None
PRIVKEY2 = None
DELEGATE = None

def link(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2, DELEGATE
	
	if param["<secret>"]:
		PUBLICKEY, PRIVKEY1 = crypto.getKeys(param["<secret>"].encode("ascii"))
		if not _checkifdelegate():
			sys.stdout.write("%s is not a valid delegate public key !\n" % PUBLICKEY)
			unlink({})
			return
		ADDRESS = crypto.getAddress(PUBLICKEY)

	DELEGATE = api.GET.delegates.get(publicKey=PUBLICKEY, returnKey="delegate")
	account = api.GET.accounts(address=ADDRESS)
	if account["success"]:
		account = account["account"]
		if account["secondSignature"] and param["<2ndSecret>"]:
			PUBKEY2, PRIVKEY2 = crypto.getKeys(param["<2ndSecret>"].encode("ascii"))
			if PUBKEY2 != account["secondPublicKey"]:
				sys.stdout.write("Incorrect second passphrase !\n")
				unlink({})
				return
	else:
		sys.stdout.write("Account does not exist in blockchain\n")
		unlink({})
		return


def unlink(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2, DELEGATE
	ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2, DELEGATE = None, None, None, None, None

def status(param):
	global ADDRESS, DELEGATE
	if ADDRESS:
		util.prettyPrint(DELEGATE)
	else:
		sys.stdout.write("No linked account\n")

def share(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2, DELEGATE

	if not ADDRESS:
		sys.stdout.write("No linked account\n")
		return
	# check second secret if needed
	account = api.GET.accounts(address=ADDRESS, returnKey="account")
	if account["secondSignature"] and not PRIVKEY2:
		PUBKEY2, PRIVKEY2 = crypto.getKeys(input("Enter your second secret : ").encode("ascii"))
		if PUBKEY2 != account["secondPublicKey"]:
			sys.stdout.write("Incorrect second passphrase !\n")
			return
	# get excluded account
	if param["--blacklist"]:
		if os.path.exists(param["--blacklist"]):
			with io.open(param["--blacklist"], "r") as in_:
				excludes = [e for e in in_.read().split() if e != ""]
		else: excludes = param["--blacklist"].split(",")
	else: excludes = []
	# get amount to share
	amount = util.floatAmount(param["<amount>"], ADDRESS)
	if param["--complement"]:
		amount = float(api.GET.accounts.getBalance(address=ADDRESS, returnKey="balance"))/100000000. - amount
	# set mini and maxi payout
	if param["--lowest"] : minimum = float(param["--lowest"])
	else: minimum = 0.
	if param["--highest"] : maximum = float(param["--highest"])
	else: maximum = amount

	if amount > 0:
		delay = int(param["--delay"])
		sys.stdout.write("Checking %s-day-true-vote-weight in transaction history...\n" % delay)
		voters = api.GET.delegates.voters(publicKey=DELEGATE["publicKey"], returnKey="accounts")
		contribution = dict([address, util.getVoteForce(address, days=delay)] for address in [voter["address"] for voter in voters] if address not in excludes)
		if maximum < amount:
			contribution = _share.ceilContribution(contribution, sum(contribution.values())*maximum/amount)
		contribution = _share.normContribution(contribution)

		round_ = util.loadJson("%s-%s.rnd" % (cfg.network, DELEGATE["username"]))
		payroll = amount * 100000000.
		minimum *= 100000000.

		transactions = []
		log = collections.OrderedDict()
		log["ADDRESS [WEIGHT]"] = "SHARE"
		for address, weight in sorted(contribution.items(), key=lambda e:e[-1], reverse=True):
			payout = payroll * weight + round_.get(address, 0.) - cfg.fees["send"]
			if payout > minimum:
				transactions.append([payout, address])
				log["%s [%.2f%%]" % (address, weight*100)] = "%s %.8f" % (cfg.token, payout/100000000.)
				round_.pop(address, None)
			elif payout != 0:
				round_[address] = payout + cfg.fees["send"]
				log["%s [%.2f%%]" % (address, weight*100)] = "%s %.8f cumuled" % (cfg.token, round_[address]/100000000.)

		if len(log):
			util.prettyPrint(log)
			if util.askYesOrNo("Validate ?"):
				for (payout, recipientId) in transactions:
					sys.stdout.write("Sending %s %.8f to %s...\n" % (cfg.token, payout/100000000, recipientId))
					payload = crypto.bakeTransaction(
						amount=payout,
						publicKey=PUBLICKEY,
						privateKey=PRIVKEY1,
						secondPrivateKey=PRIVKEY2,
						recipientId=recipientId,
					)
					util.prettyPrint(api.post("/peer/transactions", transactions=[payload]), log=True)
				util.dumpJson(round_, "%s.rnd" % DELEGATE["username"])
			else:
				sys.stdout.write("Broadcast canceled\n")

# --------------
def _whereami():
	if ADDRESS:
		return "delegate[%s]" % util.shortAddress(ADDRESS)
	else:
		return "delegate"

def _checkifdelegate():
	global DELEGATE

	i = 0
	search = api.GET.delegates(offset=i*201, limit=201, returnKey='delegates')
	while len(search) >= 201:
		i += 1
		if len([d for d in search if d["publicKey"] == PUBLICKEY]): return True
		else: search = api.GET.delegates(offset=i*201, limit=201, returnKey='delegates')

	return False
