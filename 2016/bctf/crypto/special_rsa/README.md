## special_rsa (crypto, 200p)


While studying and learning RSA, I knew a new form of encryption/decryption with the same safety as RSA.
I encrypted msg.txt and got msg.enc as an example for you.
```shell
$ python special_rsa.py enc msg.txt msg.enc
```
Can you recover flag.txt from flag.enc?  
[special_rsa.zip.f6e85b8922b0016d64b1d006529819de](./special_rsa.zip.f6e85b8922b0016d64b1d006529819de)

---------------------------------------

### step 1
Analyzing the `special_rsa.py` src code, we know the key is `k` or `k_inv`. If we know the one of them, problem is solved.
```python
def decrypt(c, k):
    out = ''
    for r_s, c_s in msgpack.unpackb(c):
        r = int(r_s.encode('hex'), 16)
        c = int(c_s.encode('hex'), 16)
        k_inv = modinv(k, N)
        out += pad_even(format(pow(k_inv, r, N) * c % N, 'x')).decode('hex')
    return out
```  

Now we get the formula `pow(k_inv, r, N) * c = m (mod N)`, and `r`, `N`, `c`, `m` are known.
we can do some change:
```python
pow(k_inv, r, N) * c = m (mod N)
pow(k_inv, r, N) * c * c_inv = m * c_inv (mod N)  # c_inv is c's Multiplicative inverse modulo (乘法逆元) 
c * c_inv = 1 (mod N)
pow(k_inv, r, N) = m * c_inv (mod N)
```

we can do a test like below: 
```python
c = inf2[0][1]
m = inf1[0]
c_inv = modinv(c, N)  
t = (m * c_inv) % N 
print (t*c)%N == m  # print true
```

### step 2
from the `msg.enc`, we can know there are two `r`, and we have: 
```python
k_inv^r1 = t1 (mod N)  # t1 = (m * c1_inv) % N
k_inv^r2 = t2 (mod N)  # t2 = (m * c2_inv) % N
```

do some change: 
```python
k_inv^(r0+r2) = t1 (mod N)  # set r1>r2 and r0+r2==r1
k_inv^r0 * k_inv^r2 = t1 (mod N)
# calc the Multiplicative inverse modulo (乘法逆元) of k_inv^r2
tmp = modinv(k_inv^r2, N) 
k_inv^r0 * k_inv^r2 * tmp = t1 * tmp (mod N)
k_inv^r0 = t1 * tmp (mod N)  # because tmp * k_inv^r2 = 1 (mod N)
```

So we get a smaller `r`. we found `r1` and `r2` are coprime, check as below：
```python
import gmpy
print gmpy.gcd(inf2[0][0], inf2[1][0]) == 1
```

so we can get the `k_inv` quickly by Euclidean algorithm (辗转相除法). like below,
```python
def my_gcd(t1, r1, t2, r2): 
    assert r1 > r2   
    r = 1     
    while r:
        r = r1 % r2
        a = r1 / r2       
        r1 = r2         
        r2 = r
        t2_inv = modinv(t2, N)
        t = t2 
        t2 = (t1*pow(t2_inv, a, N)) % N
        t1 = t 
    # print t1, r1 
    # print t2, r2 
    assert r1 == 1
    return t1
    
t1, r1 = lst[0]
t2, r2 = lst[1]
if r1 >= r2:
    k_inv = my_gcd(t1, r1, t2, r2)
else:
    k_inv = my_gcd(t2, r2, t1, r1)
```

Great! we get the `k_inv`. See all the code in [special_rsa_ans.py](./special_rsa_ans.py)