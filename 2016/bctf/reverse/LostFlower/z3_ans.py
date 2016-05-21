from z3 import *

table = [0, 
	0x00000001,
	0x00000400,
	0x0000e6a9,
	0x00100000,
	0x009502f9,
	0x039aa400,
	0x10d63af1,
	0x40000000,
	0xcfd41b91,
	]

s = Solver()
num = [BitVec("x%s" % i, 32) for i in range(10)]
y = [BitVec("y%s" % i, 32) for i in range(10)]

for i in range(0, 9):
	s.add(num[i]>=0, num[i]<=9)
s.add(num[9]>=0, num[9]<=2)

a = 0
b = 0
for i in range(10):
	a += num[i] * 10**i
	b += y[i]

# print a 
# print b  

for i in range(10):
	s.add([If(num[i] == j, y[i] == table[j], True) for j in range(10)])

s.add(a - b == 0x80000000)

assert(s.check() == sat)

m = s.model()
res = []
for i in range(10):
    # res.append(str(m[num[i]].as_long()))
    res.append(str(m.evaluate(num[i])))
res = res[::-1]
print "".join(res)

