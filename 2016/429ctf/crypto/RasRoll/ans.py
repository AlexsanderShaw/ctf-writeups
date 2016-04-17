
p = 18443
q = 49891
N = 920139713
d = 96849619

fin = open("data.txt")
fin.readline()
fin.readline()

res = []
for a in fin:
	c = int(a)
	res.append(chr(pow(c, d, N)))
print "".join(res)