from ctypes import *

##prompt = [0x76, 0x5e, 0x5e, 0x55, 0x10]
##prompt = [chr(ch^0x31) for ch in prompt]
##print "".join(prompt)

res = [ 0x6C, 0xCE, 0x26, 0xDC, 0x25, 0xC6, 0xB6, 0xD8,
        0x19, 0x73, 0x90, 0xED, 0x3B, 0xA6, 0xC6, 0x03]

res = [ch^0x31 for ch in res]

AAA = [0x00112233, 0x44556677, 0x8899AABB, 0xCCDDEEFF]

def decode(v, k):  
    t0 = c_uint(v[0])
    t1 = c_uint(v[1])
    delta = 0x61c88647  
    n = 128  
    w = [0, 0]  
    sum = c_uint(0)
    for i in range(n): sum.value -= delta
    while n > 0:
        t1.value -= (sum.value + t0.value) ^ (k[2] + (t0.value<<4)) ^ (k[3] + (t0.value>>5))
        t0.value -= (sum.value + t1.value) ^ (k[0] + (t1.value<<4)) ^ (k[1] + (t1.value>>5))
        sum.value += delta 
        n -= 1
    assert (sum.value == 0)
    w[0] = t0.value 
    w[1] = t1.value
    return w

def toInt(v):
    return v[0] + (v[1]<<8) + (v[2]<<16) + (v[3]<<24)

def toChar(n):
    v = [0, 0, 0, 0]
    v[0] = (n >> 24) & 0xff
    v[1] = (n >> 16) & 0xff
    v[2] = (n >> 8) & 0xff
    v[3] = n & 0xff
    return v

def chg(n):
    if n<10:
        return chr(48+n)
    else:
        return chr(87+n)

##print [hex(ch) for ch in res]
##print hex(toInt(res))
v1 = [toInt(res[0:4]), toInt(res[4:8])]
v2 = [toInt(res[8:12]), toInt(res[12:16])]
##print v1, v2
w1 = decode(v1, AAA)
w2 = decode(v2, AAA)

##print w1
##print w2

ans = []
for n in [w1[0], w1[1], w2[0], w2[1]]:
    ans.extend(toChar(n))
##print [hex(ch) for ch in ans]

lst = []
for ch in ans:
    lst.append(chg(ch>>4))
    lst.append(chg(ch&0xf))
    
print ''.join(lst)

