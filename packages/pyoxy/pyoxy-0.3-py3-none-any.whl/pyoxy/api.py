# -*- encoding: utf8 -*-
# © Toons

from . import __PY3__, __FROZEN__, ROOT, HOME
if not __PY3__: import cfg, slots
else: from . import cfg, slots

import io, os, sys, json, random, requests, logging, traceback

__TIMEOUT__ = 3
POST, PUT, GET = [], [], []
PEERS = []

#################
## API methods ##
#################

def get(entrypoint, dic={}, **kw):
	"""
generic GET call using requests lib. It returns server response as dict object.
It uses default peers registered in SEEDS list.

Argument:
entrypoint (str) -- entrypoint url path

Keyword argument:
dic (dict) -- api parameters as dict type
**kw       -- api parameters as keyword argument (overwriting dic ones)

Returns dict
"""
	# merge dic and kw values
	args = dict(dic, **kw)
	# API response contains several fields and wanted one can be extracted using
	# a returnKey that match the field name
	returnKey = args.pop("returnKey", False)
	args = dict([k.replace("and_", "AND:") if k.startswith("and_") else k, v] for k,v in args.items())
	try:
		text = requests.get(
			args.get("peer", random.choice(cfg.peers)) + entrypoint,
			params=args,
			headers=cfg.headers,
			verify=cfg.verify,
			timeout=__TIMEOUT__
		).text
		data = json.loads(text)
	except Exception as error:
		data = {"success":False, "error":error}
		if hasattr(error, "__traceback__"):
			data["details"] = "\n"+("".join(traceback.format_tb(error.__traceback__)).rstrip())
	else:
		if data["success"]:
			data = data[returnKey] if returnKey in data else data
	return data

def post(entrypoint, dic={}, **kw):
	# merge dic and kw values
	payload = dict(dic, **kw)
	# API response contains several fields and wanted one can be extracted using
	# a returnKey that match the field name
	returnKey = payload.pop("returnKey", False)
	try:
		text = requests.post(
			random.choice(cfg.peers) + entrypoint,
			data=json.dumps(payload),
			headers=cfg.headers,
			verify=cfg.verify,
			timeout=__TIMEOUT__
		).text
		data = json.loads(text)
	except Exception as error:
		sys.stdout.write(text + "\n")
		data = {"success":False, "error":error}
		if hasattr(error, "__traceback__"):
			data["details"] = "\n"+("".join(traceback.format_tb(error.__traceback__)).rstrip())
	return data

def put(entrypoint, dic={}, **kw):
	# merge dic and kw values
	payload = dict(dic, **kw)
	# API response contains several fields and wanted one can be extracted using
	# a returnKey that match the field name
	returnKey = payload.pop("returnKey", False)
	try:
		text = requests.put(
			random.choice(cfg.peers) + entrypoint,
			data=json.dumps(payload),
			headers=cfg.headers,
			verify=cfg.verify,
			timeout=__TIMEOUT__
		).text
		data = json.loads(text)
	except Exception as error:
		sys.stdout.write(text + "\n")
		data = {"success":False, "error":error}
		if hasattr(error, "__traceback__"):
			data["details"] = "\n"+("".join(traceback.format_tb(error.__traceback__)).rstrip())
	return data

#################
## API wrapper ##
#################

class Endpoint:
	
	def __init__(self, method, endpoint):
		self.method = method
		self.endpoint = endpoint

	def __call__(self, dic={}, **kw):
		return self.method(self.endpoint, dic, **kw)

	@staticmethod
	def createEndpoint(ndpt, method, path):
		elem = path.split("/")
		end = elem[-1]
		path = "/".join(elem[:2])
		for name in elem[2:]:
			path += "/"+name
			if not hasattr(ndpt, name):
				setattr(ndpt, name, Endpoint(method, path))
			ndpt = getattr(ndpt, name)

def loadEntrypoints(network):
	global POST, PUT, GET

	try:
		in_ = io.open(os.path.join(ROOT, "%s.ntpt"%network), "r" if __PY3__ else "rb")
		entrypoints = json.load(in_)
		in_.close()
	except FileNotFoundError:
		sys.stdout.write("No entrypoints file found\n")
		return False

	POST = Endpoint(post, "/api")
	for endpoint in entrypoints["POST"]:
		POST.createEndpoint(POST, post, endpoint)

	PUT = Endpoint(put, "/api")
	for endpoint in entrypoints["PUT"]:
		PUT.createEndpoint(PUT, put, endpoint)

	GET = Endpoint(get, "/api")
	for endpoint in entrypoints["GET"]:
		GET.createEndpoint(GET, get, endpoint)

	return True

#######################
## network selection ##
#######################

def use(network):
	networks = [os.path.splitext(name)[0] for name in os.listdir(ROOT) if name.endswith(".net")]

	if len(networks) and network in networks:
		in_ = open(os.path.join(ROOT, network+".net"), "r" if __PY3__ else "rb")
		data = json.load(in_)
		in_.close()
		cfg.__dict__.update(data)
		cfg.verify = os.path.join(os.path.dirname(sys.executable), "cacert.pem") if __FROZEN__ else True
		cfg.begintime = slots.datetime.datetime(*cfg.begintime, tzinfo=slots.pytz.UTC)
		# create entrypoints
		if loadEntrypoints(network):
			# update fees
			cfg.fees = GET.blocks.getFees(returnKey="fees")
			#update headers
			cfg.headers["version"] = GET.peers.version(returnKey="version")
			cfg.headers["nethash"] = GET.blocks.getNethash(returnKey="nethash")
			cfg.network = network
			cfg.hotmode = True
		
	else:
		raise NetworkError("Unknown %s network properties" % network)
		cfg.network = "..."
		cfg.hotmode = False

	# update logger data so network appear on log
	logger = logging.getLogger()
	logger.handlers[0].setFormatter(logging.Formatter('[%s]'%network + '[%(asctime)s] %(message)s'))
