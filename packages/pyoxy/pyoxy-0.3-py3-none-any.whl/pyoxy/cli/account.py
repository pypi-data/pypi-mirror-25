# -*- encoding: utf8 -*-
# © Toons

'''
Usage: account link <secret> [<2ndSecret>]
       account unlink
       account status
       account send <amount> <address>

Subcommands:
    link     : link to account using secret passphrases. If secret passphrases
               contains spaces, it must be enclosed within double quotes
               ("secret with spaces").
    unlink   : unlink account.
    status   : show information about linked account.
    send     : send OXY amount to address.
'''

from .. import ROOT, cfg, api, util, crypto

import io, os, sys

ADDRESS = None
PUBLICKEY = None
PRIVKEY1 = None
PRIVKEY2 = None

def link(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2
	
	if param["<secret>"]:
		PUBLICKEY, PRIVKEY1 = crypto.getKeys(param["<secret>"].encode("ascii"))
		ADDRESS = crypto.getAddress(PUBLICKEY)

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
		return

def unlink(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2
	ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2 = None, None, None, None

def status(param):
	if ADDRESS:
		util.prettyPrint(api.GET.accounts(address=ADDRESS, returnKey="account"))
	else:
		sys.stdout.write("No linked account\n")

def send(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2

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

	payload = crypto.bakeTransaction(
		amount=util.floatAmount(param["<amount>"], ADDRESS)*100000000,
		publicKey=PUBLICKEY,
		privateKey=PRIVKEY1,
		secondPrivateKey=PRIVKEY2,
		recipientId=param["<address>"],
	)
	payload["address"] = ADDRESS

	if util.askYesOrNo("Broadcast %s?" % util.reprTransaction(payload)):
		sys.stdout.write("Sending %s %.8f to %s...\n" % (cfg.token, payload["amount"]/100000000, payload["recipientId"]))
		util.prettyPrint(api.post("/peer/transactions", transactions=[payload]), log=True)
	else:
		sys.stdout.write("Broadcast canceled\n")
		return

# --------------
def _whereami():
	if ADDRESS:
		return "account[%s]" % util.shortAddress(ADDRESS)
	else:
		return "account"
