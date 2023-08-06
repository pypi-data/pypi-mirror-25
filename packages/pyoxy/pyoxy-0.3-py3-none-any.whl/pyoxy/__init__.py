# -*- encoding: utf8 -*-
# © Toons
__version__ = "0.3"

import os, imp, sys, logging, requests

__PY3__ = True if sys.version_info[0] >= 3 else False
__FROZEN__ = hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")

logging.getLogger('requests').setLevel(logging.CRITICAL)

# deal with home and root directory
ROOT = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if __FROZEN__ else __file__)))
try: HOME = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
except: HOME = os.environ.get("HOME", ROOT)

# setup a log file
logging.basicConfig(
	filename  = os.path.normpath(os.path.join(ROOT, __name__+".log")) if __FROZEN__ else os.path.normpath(os.path.join(HOME, "."+__name__)),
	format    = '[...][%(asctime)s] %(message)s',
	level     = logging.INFO,
)
