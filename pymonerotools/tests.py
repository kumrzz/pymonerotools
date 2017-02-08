from toolz import *

def test1():
    randseedphrase = monerorandseedphrase()
    seedhex = recoverSK(randseedphrase)
    #seedhex = monerorandseedhex()
    prvviewkey = prvviewkeyfrmhexseed(seedhex)
    prvspendkeyreduced = sc_reduce_key(seedhex)
    PublicSpendKey = publicFromSecret(prvspendkeyreduced)
    PublicViewKey = publicFromSecret(prvviewkey)
    pubaddress = encode_addr(12, PublicSpendKey, PublicViewKey)

    """
    testsk = monerorandseedhex()
    testseedraw = mn_encode(testsk)
    testseed = testseedraw + ' ' + electrumChecksum(testseedraw)
    print 'test seed: ', testseed
    seedhex1 = recoverSK(testseed)
    print 'test seed', seedhex1
    print 'orig seed', testsk
    print ' '
    """

    print 'seed phrase: ', '\n', randseedphrase
    print 'seed(hex) is: ', seedhex
    print 'priv spendkey reduced: ', prvspendkeyreduced
    print 'public spend key: ', PublicSpendKey
    print 'private view key: ', prvviewkey
    print 'public view key: ', PublicViewKey
    print 'public address: ', pubaddress