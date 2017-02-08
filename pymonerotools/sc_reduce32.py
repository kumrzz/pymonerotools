# This is an attempt to make a real version of sc_reduce32,
# to match exactly the behavior in in:
#https://github.com/monero-project/monero/blob/master/src/crypto/crypto-ops.c
#lifted from http://codegists.com/snippet/python/sc_reduce32py_rlittlefield_python

def loadN(b, n, index):
    base = 0;
    result = 0
    for i in range(n):
        byte = b[index + i]
        result |= (byte << base)
        base += 8
    return result;


def sc_reduce32(b):
    s0 = 2097151 & loadN(b, 3, 0)
    s1 = 2097151 & (loadN(b, 4, 2) >> 5)
    s2 = 2097151 & (loadN(b, 3, 5) >> 2)
    s3 = 2097151 & (loadN(b, 4, 7) >> 7)
    s4 = 2097151 & (loadN(b, 4, 10) >> 4)
    s5 = 2097151 & (loadN(b, 3, 13) >> 1)
    s6 = 2097151 & (loadN(b, 4, 15) >> 6)
    s7 = 2097151 & (loadN(b, 3, 18) >> 3)
    s8 = 2097151 & loadN(b, 3, 21)
    s9 = 2097151 & (loadN(b, 4, 23) >> 5)
    s10 = 2097151 & (loadN(b, 3, 26) >> 2)
    s11 = (loadN(b, 4, 28) >> 7)
    s12 = 0

    carry0 = (s0 + (1 << 20)) >> 21;
    s1 += carry0;
    s0 -= carry0 << 21;
    carry2 = (s2 + (1 << 20)) >> 21;
    s3 += carry2;
    s2 -= carry2 << 21;
    carry4 = (s4 + (1 << 20)) >> 21;
    s5 += carry4;
    s4 -= carry4 << 21;
    carry6 = (s6 + (1 << 20)) >> 21;
    s7 += carry6;
    s6 -= carry6 << 21;
    carry8 = (s8 + (1 << 20)) >> 21;
    s9 += carry8;
    s8 -= carry8 << 21;
    carry10 = (s10 + (1 << 20)) >> 21;
    s11 += carry10;
    s10 -= carry10 << 21;

    carry1 = (s1 + (1 << 20)) >> 21;
    s2 += carry1;
    s1 -= carry1 << 21;
    carry3 = (s3 + (1 << 20)) >> 21;
    s4 += carry3;
    s3 -= carry3 << 21;
    carry5 = (s5 + (1 << 20)) >> 21;
    s6 += carry5;
    s5 -= carry5 << 21;
    carry7 = (s7 + (1 << 20)) >> 21;
    s8 += carry7;
    s7 -= carry7 << 21;
    carry9 = (s9 + (1 << 20)) >> 21;
    s10 += carry9;
    s9 -= carry9 << 21;
    carry11 = (s11 + (1 << 20)) >> 21;
    s12 += carry11;
    s11 -= carry11 << 21;

    s0 += s12 * 666643;
    s1 += s12 * 470296;
    s2 += s12 * 654183;
    s3 -= s12 * 997805;
    s4 += s12 * 136657;
    s5 -= s12 * 683901;
    s12 = 0;

    carry0 = s0 >> 21;
    s1 += carry0;
    s0 -= carry0 << 21;
    carry1 = s1 >> 21;
    s2 += carry1;
    s1 -= carry1 << 21;
    carry2 = s2 >> 21;
    s3 += carry2;
    s2 -= carry2 << 21;
    carry3 = s3 >> 21;
    s4 += carry3;
    s3 -= carry3 << 21;
    carry4 = s4 >> 21;
    s5 += carry4;
    s4 -= carry4 << 21;
    carry5 = s5 >> 21;
    s6 += carry5;
    s5 -= carry5 << 21;
    carry6 = s6 >> 21;
    s7 += carry6;
    s6 -= carry6 << 21;
    carry7 = s7 >> 21;
    s8 += carry7;
    s7 -= carry7 << 21;
    carry8 = s8 >> 21;
    s9 += carry8;
    s8 -= carry8 << 21;
    carry9 = s9 >> 21;
    s10 += carry9;
    s9 -= carry9 << 21;
    carry10 = s10 >> 21;
    s11 += carry10;
    s10 -= carry10 << 21;
    carry11 = s11 >> 21;
    s12 += carry11;
    s11 -= carry11 << 21;

    s0 += s12 * 666643;
    s1 += s12 * 470296;
    s2 += s12 * 654183;
    s3 -= s12 * 997805;
    s4 += s12 * 136657;
    s5 -= s12 * 683901;

    carry0 = s0 >> 21;
    s1 += carry0;
    s0 -= carry0 << 21;
    carry1 = s1 >> 21;
    s2 += carry1;
    s1 -= carry1 << 21;
    carry2 = s2 >> 21;
    s3 += carry2;
    s2 -= carry2 << 21;
    carry3 = s3 >> 21;
    s4 += carry3;
    s3 -= carry3 << 21;
    carry4 = s4 >> 21;
    s5 += carry4;
    s4 -= carry4 << 21;
    carry5 = s5 >> 21;
    s6 += carry5;
    s5 -= carry5 << 21;
    carry6 = s6 >> 21;
    s7 += carry6;
    s6 -= carry6 << 21;
    carry7 = s7 >> 21;
    s8 += carry7;
    s7 -= carry7 << 21;
    carry8 = s8 >> 21;
    s9 += carry8;
    s8 -= carry8 << 21;
    carry9 = s9 >> 21;
    s10 += carry9;
    s9 -= carry9 << 21;
    carry10 = s10 >> 21;
    s11 += carry10;
    s10 -= carry10 << 21;
    s = []

    myint = 0

    items = []
    items.append(s0 >> 0)
    items.append(s0 >> 8)
    items.append((s0 >> 16) | (s1 << 5))
    items.append(s1 >> 3)
    items.append(s1 >> 11)
    items.append((s1 >> 19) | (s2 << 2))
    items.append(s2 >> 6)
    items.append((s2 >> 14) | (s3 << 7))
    items.append(s3 >> 1)
    items.append(s3 >> 9)
    items.append((s3 >> 17) | (s4 << 4))
    items.append(s4 >> 4)
    items.append(s4 >> 12)
    items.append((s4 >> 20) | (s5 << 1))
    items.append(s5 >> 7)
    items.append((s5 >> 15) | (s6 << 6))
    items.append(s6 >> 2)
    items.append(s6 >> 10)
    items.append((s6 >> 18) | (s7 << 3))
    items.append(s7 >> 5)
    items.append(s7 >> 13)
    items.append(s8 >> 0)
    items.append(s8 >> 8)
    items.append((s8 >> 16) | (s9 << 5))
    items.append(s9 >> 3)
    items.append(s9 >> 11)
    items.append((s9 >> 19) | (s10 << 2))
    items.append(s10 >> 6)
    items.append((s10 >> 14) | (s11 << 7))
    items.append(s11 >> 1)
    items.append(s11 >> 9)
    items.append(s11 >> 17)

    newb = b''
    for i in items:
        tmp = i.to_bytes((i.bit_length() + 7) // 8, byteorder='little')
        localnewbyte = bytes([tmp[0]])
        newb += localnewbyte
    return newb