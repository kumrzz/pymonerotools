#!/usr/bin/env python
#ripp'ed and adapted from: https://github.com/spesmilo/electrum/blob/master/lib/mnemonic.py
import os
import math
import unicodedata
import binascii #conversion between hex, int, and binary. Also for the crc32 thing

import Crypto.Random.random as cryptorandom
import zlib
import Keccak, ed25519#in this library

from electrum.util import print_error

netVersion = '12'#network byte:12 for mainnet, 35 for testnet

# http://www.asahi-net.or.jp/~ax2s-kmtn/ref/unicode/e_asia.html
CJK_INTERVALS = [
    (0x4E00, 0x9FFF, 'CJK Unified Ideographs'),
    (0x3400, 0x4DBF, 'CJK Unified Ideographs Extension A'),
    (0x20000, 0x2A6DF, 'CJK Unified Ideographs Extension B'),
    (0x2A700, 0x2B73F, 'CJK Unified Ideographs Extension C'),
    (0x2B740, 0x2B81F, 'CJK Unified Ideographs Extension D'),
    (0xF900, 0xFAFF, 'CJK Compatibility Ideographs'),
    (0x2F800, 0x2FA1D, 'CJK Compatibility Ideographs Supplement'),
    (0x3190, 0x319F , 'Kanbun'),
    (0x2E80, 0x2EFF, 'CJK Radicals Supplement'),
    (0x2F00, 0x2FDF, 'CJK Radicals'),
    (0x31C0, 0x31EF, 'CJK Strokes'),
    (0x2FF0, 0x2FFF, 'Ideographic Description Characters'),
    (0xE0100, 0xE01EF, 'Variation Selectors Supplement'),
    (0x3100, 0x312F, 'Bopomofo'),
    (0x31A0, 0x31BF, 'Bopomofo Extended'),
    (0xFF00, 0xFFEF, 'Halfwidth and Fullwidth Forms'),
    (0x3040, 0x309F, 'Hiragana'),
    (0x30A0, 0x30FF, 'Katakana'),
    (0x31F0, 0x31FF, 'Katakana Phonetic Extensions'),
    (0x1B000, 0x1B0FF, 'Kana Supplement'),
    (0xAC00, 0xD7AF, 'Hangul Syllables'),
    (0x1100, 0x11FF, 'Hangul Jamo'),
    (0xA960, 0xA97F, 'Hangul Jamo Extended A'),
    (0xD7B0, 0xD7FF, 'Hangul Jamo Extended B'),
    (0x3130, 0x318F, 'Hangul Compatibility Jamo'),
    (0xA4D0, 0xA4FF, 'Lisu'),
    (0x16F00, 0x16F9F, 'Miao'),
    (0xA000, 0xA48F, 'Yi Syllables'),
    (0xA490, 0xA4CF, 'Yi Radicals'),
]

def is_CJK(c):
    n = ord(c)
    for imin,imax,name in CJK_INTERVALS:
        if n>=imin and n<=imax: return True
        return False

filenames = {
    'en':'english.txt',
    'es':'spanish.txt',
    'ja':'japanese.txt',
    'pt':'portuguese.txt',
    'zh':'chinese_simplified.txt'
}


class Mnemonic(object):
    # Seed derivation no longer follows BIP39
    # Mnemonic phrase uses a hash based checksum, instead of a wordlist-dependent checksum

    def __init__(self, lang=None):
        lang = lang or 'en'
        print_error('language', lang)
        filename = filenames.get(lang[0:2], 'english.txt')
        path = os.path.join(os.path.dirname(__file__), 'wordlist', filename)
        s = open(path,'r').read().strip()
        s = unicodedata.normalize('NFKD', s.decode('utf8'))
        lines = s.split('\n')
        self.wordlist = []
        for line in lines:
            line = line.split('#')[0]
            line = line.strip(' \r')
            assert ' ' not in line
            if line:
                self.wordlist.append(line)
        print_error("wordlist has %d words"%len(self.wordlist))
#end of Class Mnemonic------------------------------


def cn_fast_hash(s):#Keccak-256 hashing
    k = Keccak.Keccak()
    return k.Keccak((len(s) * 4, s), 1088, 512, 32 * 8, False).lower()
    #r = bitrate = 1088, c = capacity, n = output length in bits


def mn_swap_endian_4byte(st):
    #this is from moneromoo's code
    #lifted from https://github.com/monero-project/mininero/blob/master/mnemonic.py
    r = st[6:8]+st[4:6]+st[2:4]+st[0:2]
    return r


def hexToInt(h):
    s = binascii.unhexlify(h) #does hex to bytes
    bb = len(h) * 4 #I guess 8 bits / b
    return sum(2**i * ed25519.bit(s,i) for i in range(0,bb)) #does to int


def intToHex(i):
    return binascii.hexlify(ed25519.encodeint(i)) #hexlify does bytes to hex


l = 2**252 + 27742317777372353535851937790883648493

def sc_reduce_key(a):
    return intToHex(hexToInt(a) % l)


def prvviewkeyfrmhexseed(sk):
    a = hexToInt(cn_fast_hash(sc_reduce_key(sk))) % l
    return intToHex(a)


def public_key(sk):
    #returns point encoded to binary .. sk is just an int..
    return ed25519.encodepoint(ed25519.scalarmultbase(sk)) #pub key is not just x coord..


def publicFromSecret(sk):
    #returns pubkey in hex, same as scalarmultBase
    return binascii.hexlify(public_key(hexToInt(sk)))


def reverseBytes(a): #input is byte string, it reverse the endianness
    b = [a[i:i+2] for i in range(0, len(a)-1, 2)]
    return ''.join(b[::-1])

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
    a = [reverseBytes(v[i:i+16]) for i in range(0, len(v)-16, 16)]
    rr = -2*((len(v) /2 )% 16)

    res = ''
    for b in a:
        bb = hexToInt(b)
        result = ''
        while bb >= __b58base:
            div, mod = divmod(bb, __b58base)
            result = __b58chars[mod] + result
            bb = div
        result = __b58chars[bb] + result
        res += result
    result = ''
    if rr < 0:
        bf =  hexToInt(reverseBytes(v[rr:])) #since we only reversed the ones in the array..
        result = ''
        while bf >= __b58base:
            div, mod = divmod(bf, __b58base)
            result = __b58chars[mod] + result
            bf = div
        result = __b58chars[bf] + result
    res += result
    return res


def addr_frmpubkeys(spendP, viewP):
    buf = netVersion + spendP + viewP#networkbyte+spendpubkey+viewpubkey
    h = cn_fast_hash(buf)##Keccak-256 hashing
    buf = buf +  h[0:8]#first 4 bytes from above appended to 'buf'
    return b58encode(buf)#Base58-encoding


def addrfrmseedhex(seedhex):#accepts Hex seed and returns public address
    privviewkey = prvviewkeyfrmhexseed(seedhex)
    privspendkey = sc_reduce_key(seedhex)
    pubspendkey = publicFromSecret(privspendkey)
    pubviewkey = publicFromSecret(privviewkey)
    return addr_frmpubkeys(pubspendkey, pubviewkey)


def mnemonic_encode(self, i):
    n = len(Mnemonic.wordlist)
    words = []
    while i:
        x = i%n
        i = i/n
        words.append(Mnemonic.wordlist[x])
    return ' '.join(words)


def mn_decode(wlist):
    # lifted from https://github.com/monero-project/mininero/blob/master/mnemonic.py
    out = ''
    words = Mnemonic().wordlist
    n = len(words)
    for i in range(len(wlist) / 3):  # note 24 / 3 = 8... 12 / 3 = 4..
        word1, word2, word3 = wlist[3 * i:3 * i + 3]
        w1 = words.index(word1)
        w2 = words.index(word2)
        w3 = words.index(word3)
        x = w1 + n * ((n + w2 - w1) % n) + n * n * ((n + w3 - w2) % n)  # as an int
        b = '%08x' % x  # this is big endian!
        out += mn_swap_endian_4byte(b)

    return out


def recoverSK(seed):
    mn2 = seed.split(" ")  # make array
    if len(mn2) > 13:
        mn2 = mn2[:24]
        sk = mn_decode(mn2)
    else:
        mn2 = mn2[:12]
        sk = cn_fast_hash(mn_decode(mn2))

    return sk


def electrumChecksum(seedinit):
    #lifted from https://github.com/monero-project/mininero/blob/master/mininero.py
    wl = seedinit.split(" ")  # make an array
    if len(wl) > 13:
        wl = wl[:24]
    else:
        wl = wl[:12]
    upl = 3  # prefix length
    wl2 = ''
    for a in wl:
        wl2 += a[:upl]
    z = ((zlib.crc32(wl2) & 0xffffffff) ^ 0xffffffff) >> 0
    z2 = ((z ^ 0xffffffff) >> 0) % len(wl)

    return wl[z2]

def integratedaddy(spendpubkey, viewpubkey, pymtIDhex=''):
    #super strange how
    net_version = '13'
    if pymtIDhex == '': pymtIDhex = randpymtidhex()
    print 'rand pymtIDhex: ' , pymtIDhex
    buf = net_version + spendpubkey + viewpubkey + pymtIDhex#networkbyte+spendpubkey+viewpubkey_pymtID
    h = cn_fast_hash(buf)##Keccak-256 hashing
    buf2 = buf +  h[0:8]#first 4 bytes from above appended to 'buf'
    return b58encode(buf2[:144])+b58encode(buf2[143:])#Base58-encoding

def addrfrmseedphrase(seedphrase):
    seedhex = recoverSK(seedphrase)
    addy = addrfrmseedhex(seedhex)
    return addy

def monerorandseedhex():#nicked from mininero.PaperWallet.skGen
    return intToHex(8 * (cryptorandom.getrandbits(64 * 8)) % l)

def randpymtidhex():
    return intToHex(cryptorandom.getrandbits(64))[:16]

def mn_encode( message ):
    out = []
    words = Mnemonic().wordlist
    n = len(words)
    for i in range(0, len(message), 8):
        message = message[0:i] + mn_swap_endian_4byte(message[i:i+8]) + message[i+8:]
    for i in range(len(message)/8):
        word = message[8*i:8*i+8]
        x = int(word, 16)
        w1 = (x%n)
        w2 = ((x//n) + w1)%n
        w3 = (((x//n)//n) + w2)%n
        out += [ words[w1], words[w2], words[w3] ]
    return ' '.join(out)


def monerorandseedphrase():
    randseed = monerorandseedhex()
    seedmnemonicraw = mn_encode(randseed)
    seedmnemonic = seedmnemonicraw + ' ' + electrumChecksum(seedmnemonicraw)
    return seedmnemonic

