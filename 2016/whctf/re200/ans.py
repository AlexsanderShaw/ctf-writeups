from z3 import *


target = [
	73767, 62102, 48910, 55372, 37336, 663,
	62102, 55344, 41766, 45072, 30247, 560,
	48910, 41766, 36843, 34717, 28867, 445,
	55372, 45072, 34717, 45069, 28239, 503,
	37336, 30247, 28867, 28239, 39900, 348,
	663, 560, 445, 503, 348, 6 ]
  
s = Solver()
flag = [BitVec('x%s'%i, 32) for i in range(27)] + [1 for _ in range(9)]


begin = "whctf{"
for i in range(len(begin)):
	s.add(flag[i] == ord(begin[i]))

s.add(flag[26] == ord('}'))

for i in range(len(begin), 26, 1):
	s.add(Or(
		And(flag[i] >= ord('A'), flag[i] <= ord('Z')), 
		And(flag[i] >= ord('a'), flag[i] <= ord('z')),
		And(flag[i] >= ord('0'), flag[i] <= ord('9')),
		flag[i] == 32,
		flag[i] == ord('_')
		))

# for i in range(len(begin), 26, 1):
# 	s.add(flag[i] >=32, flag[i] <= 126)

BBB = [0 for _ in range(36)]
for i in range(6):
	for j in range(6):
		BBB[j*6 + i] = flag[i*6 + j]


AAA = [0 for _ in range(36)]
for i in range(6):
	for j in range(6):
		for k in range(6):
			AAA[i*6 + j] += flag[i*6+k]*BBB[k*6+j]

for i in range(36):
	s.add(AAA[i] == target[i])

assert(s.check() == sat) 

m = s.model()
res = []
for i in range(27):
    res.append(chr(m[flag[i]].as_long()))
print ''.join(res)


# output is below:
# whctf{Y0u_ar3_g00d_a7_m4th}