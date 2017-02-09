<b>work in progress!!</b>
Trying to emulate the C++ code for monero core using python, with tools like Pybitcointools does.
only supports the english word list at the moment, only tested in python2.7

:Info: Probably a good lightweight python paperwallet generator that you can be sure doesn't 'phone home'

to install using pip::
    ``pip install https://github.com/kumrzz/pymonerotools/zipball/master``

Generate random seed phrase(mnemonic)::
    ``pymonerotools.toolz.monerorandseedphrase()``

Generate random hex seed::
    ``pymonerotools.toolz.monerorandseedhex()``

Find public address from seedphrase(mnemonic)::
    ``pymonerotools.toolz.addrfrmseedphrase(raw_input('enter your seedphrase>>'))``

Recover hex seed from mnemonic seedphrase::
    ``pymonerotools.toolz.recoverSK(raw_input('enter your seedphrase>>'))``
