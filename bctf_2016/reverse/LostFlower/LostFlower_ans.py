# -*- coding:utf-8 -*-
'''
Created on Mar 21, 2016

@author: czl
'''


def force():
	lst = range(10)
	for a1 in [1, 2]:
		for a2 in lst:
			for a3 in lst:
				for b1 in lst:
					for b2 in lst:
						for b3 in lst:
							for c1 in lst:
								for c2 in lst:
									for c3 in lst:
										for d1 in lst:
											yield (a1, a2, a3, b1, b2, b3, c1, c2, c3, d1)
											


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


# if abs(x) < 0 is true, then x is 0x80000000
print "start"
for a1, a2, a3, b1, b2, b3, c1, c2, c3, d1 in force():
	target = a1*1000000000 + a2*100000000 + a3*10000000 + \
			 b1*1000000 + b2*100000 + b3*10000 + \
			 c1*1000 + c2*100 + c3*10 + d1
	sum = table[a1] + table[a2] + table[a3] + \
		  table[b1] + table[b2] + table[b3] + \
		  table[c1] + table[c2] + table[c3] + \
		  table[d1] 

	sum = sum & 0xffffffff
	if (target - sum) & 0xffffffff == 0x80000000:
		print "equ find.."
		print a1, a2, a3, b1, b2, b3, c1, c2, c3, d1
		print target
		print sum
		break

print "over"

# output is below:
# start
# equ find..
# 1 4 2 2 4 4 5 9 5 6
# 1422445956
# 3569929604
# over

# put the 1422445956 into app, we can get the flag.
# BCTF{wrhav3f4nwxo}
