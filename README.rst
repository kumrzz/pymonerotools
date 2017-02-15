**work in progress!!**
Trying to emulate the C++ code for monero core using python, with tools like Pybitcointools does.
only supports the english word list at the moment, only tested in python2.7

:Info: Probably a good lightweight python paperwallet generator that you can be sure doesn't 'phone home'

to install using pip::
    ``pip install https://github.com/kumrzz/pymonerotools/zipball/master``

Generate random seed phrase(mnemonic)::
    ``pymonerotools.monerorandseedphrase()``

Generate random hex seed::
    ``pymonerotools.monerorandseedhex()``

Find public address from seedphrase(mnemonic)::
    ``pymonerotools.addrfrmseedphrase(raw_input('enter your seedphrase>>'))``

Recover hex seed from mnemonic seedphrase::
    ``pymonerotools.recoverSK(raw_input('enter your seedphrase>>'))``  

Generate random paymentID(64bit, 16hex chars)::
    ``pymonerotools.randpaymentidhex()``

Generate integrated address from public(spend+view)keys and paymentID::
    ``pymonerotools.integratedaddrgen('0c2cce26e193b88a96aed3fa250225b286fd670acf0dcb7dceaf683e990fa315', 'c0d1fc8e35ff76b94f9d554390f6662fcabc2dc00801ed6f9199926dd9ac17be', 'e9498879a27f6042')``

### Listing of main commands:  

* monerorandseedphrase  : () -> random seed phrase (mnemonic)  
* monerorandseedhex     : () -> random seed in hexadecimal format  
* addrfrmseedphrase     : (seedphrase) -> (regular) monero public address, 2nd param(if supplied) for networktype: testnet or mainnet  
* recoverSK             : (seedphrase) -> seedphrase converted to hexadecimal format  
* randpaymentidhex      : () -> random paymentID(64bit, 16hex chars) in hexadecimal format  
* integratedaddrgen     : (pubspendkey, pubviewkey, pamentID) -> integrated monero address[additional param(if supplied) for networktype: testnet or mainnet]  
