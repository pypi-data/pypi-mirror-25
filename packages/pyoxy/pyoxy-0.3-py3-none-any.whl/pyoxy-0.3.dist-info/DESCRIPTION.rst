Copyright 2017 **Toons**, `MIT licence`_

Install
=======

Ubuntu / OSX
^^^^^^^^^^^^

>From development version

``sudo -H pip install git+https://github.com/Moustikitos/oxycoin.git``

If you work with ``python3``

``sudo -H pip3 install git+https://github.com/Moustikitos/oxycoin.git``

Windows 
^^^^^^^

>From development version

``pip install git+https://github.com/Moustikitos/oxycoin.git``

Using ``pyoxy``
===============

*Compatibility with lisk and shift is not fully supported at the moment, if you go there you're on your own !*

Use Oxycoin API
^^^^^^^^^^^^^^^

``api`` module allows developpers to send requests to the blockchain. For
security reason only run ``POST`` and ``PUT`` entrypoints from blockchain node.

>>> from pyoxy import api
>>> api.use("toxy") # work on testnet

All entrypoints can be reach using this syntax :

``api.[METHOD].[entrypoint with "/" replaced by "."](param=value, ...[returnKey=name])``

>>> # http equivalent [PEER ADDRESS]/api/delegates/get?username=toons
>>> api.GET.delegates.get(username="toons")
{'delegate': {'address': '12773656026018032534X', 'vote': '50649323252343', 'pub
licKey': '926f731a0fbc04d845fe10f6d4917c47317704af55151c08e07be6616220ddaf', 'us
ername': 'toons', 'rank': 28, 'rate': 28, 'approval': 0.5, 'producedblocks': 154
, 'missedblocks': 0, 'productivity': 100}, 'success': True}

It returns a python dictionary transposed from server json response. You can
provide a ``returnKey`` option value to get the field you want from server response

>>> api.GET.delegates.get(username="toons", returnKey="delegate")
{'address': '12773656026018032534X', 'vote': '50649323252343', 'publicKey': '926
f731a0fbc04d845fe10f6d4917c47317704af55151c08e07be6616220ddaf', 'username': 'too
ns', 'rank': 28, 'rate': 28, 'approval': 0.5, 'producedblocks': 154, 'missedbloc
ks': 0, 'productivity': 100}

Send Oxycoin
^^^^^^^^^^^^

``pyoxy`` bakes transaction localy using ``pynacl`` crypto library so no secret is
sent trough the network. only ``type-0`` transaction can be broadcasted for now.
Amount is given in SATOSHI.

>>> from pyoxy import api, util
>>> api.use("toxy") 
>>> util.sendTransaction(amount=100000000, recipientId="15981732227677853647X", secret="your secret")
{'success': True}

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

You can use ``pyoxy`` package without writing a line of code trough command
line interface. There are two ways to launch the CLI.

**from command line**

``python -m pyoxy-cli``

**from python code**

>>> from pyoxy import cli
>>> cli.start()
Welcome to pyoxy-cli [Python 3.5.1 / pyoxy 0.1b]
Available commands: network, account, delegate
cold@.../>

**How to send Oxycoins ?**

>>> from pyoxy import cli
>>> cli.start()
Welcome to pyoxy-cli [Python 3.5.1 / pyoxy 0.1b]
Available commands: network, account, delegate
cold@.../> network use
Network(s) found:
    1 - lisk
    2 - oxy
    3 - shift
    4 - toxy
Choose an item: [1-4]> 4
hot@toxy/network> account link "your secret with spaces between quotes"
hot@toxy/account[15600...1854X]> send 1.1235 12427608128403844156X
{'success': True}

**How to run a pool ?**

>>> from pyoxy import cli
>>> cli.start()
Welcome to pyoxy-cli [Python 3.5.1 / pyoxy 0.1b]
Available commands: network, account, delegate
cold@.../> network use
Network(s) found:
    1 - lisk
    2 - oxy
    3 - shift
    4 - toxy
Choose an item: [1-4]> 4
hot@toxy/network> delegate link "your secret with spaces between quotes"
hot@toxy/account[15600...1854X]> share <amoun> --options=values

+ ``<amount>`` value can be:
   * relative value ie 10% of account balance
   * absolute value using decimal numbers 45.6
   * fiat ($60, Â£41, â‚¬62 or Â¥125) value converted using ``coinmarketcap`` API
+ ``options`` can be :
   * ``-b`` or ``--blacklist`` a coma-separated-address-list or a full path to newline-separated-address file
   * ``-d`` or ``--delay`` the number of day you want to analyse voters behaviour
   * ``-l`` or ``--lowest`` the treshold payout to trigger payment (unpaid payout are saved)
   * ``-h`` or ``--highest`` the ceiling payout

Graphical user interface (python 3.x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the pyoxy payout user interface: ``python -m pyoxy-ui``

.. image:: https://github.com/Moustikitos/oxycoin/raw/master/pyoxy-ui.png

Authors
=======

Toons <moustikitos@gmail.com>

Support this project
====================

+ Toons Bitcoin address: ``1qjHtN5SuzvcA8RZSxNPuf79iyLaVjxfc``
+ Toons Oxycoin address: ``12427608128403844156X``
+ Vote for **toons** delegate on oxycoin blockchain

Version
=======

**0.3**

+ Added ``lisk`` and ``shift`` network

**0.2**

+ ``ui`` pkg released

**0.1**

+ ``api`` mod released
+ ``crypto`` mod released
+ ``util`` mod released
+ ``cli`` pkg released

.. _MIT licence: http://htmlpreview.github.com/?https://github.com/Moustikitos/oxycoin/blob/master/pyoxy.html
.. role:: red


