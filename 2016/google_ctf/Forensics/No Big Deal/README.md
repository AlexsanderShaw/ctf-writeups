##题目描述
---

题目给的一个`tcpdump capture file`:

[no-big-deal.pcap](./no-big-deal.pcap)


##题解
---
当我翻墙下载下来这个big file的时候，看了一下大小.

```
➜  Desktop  ls -lh no-big-deal.pcap
-rw-r--r--@ 1 shellvon  staff    96M  4 30 19:27 no-big-deal.pcap
```
第一想法是好大哦，我第一次遇见这么大的文件，要不strings看看(strings估计也很多，我们看一下长的吧)..

然后

```bash
strings no-big-deal.pcap | grep -E "[a-zA-Z0-9_]{15,}"
```


我看到有许多是属于rb结尾的ruby文件和mod文件和最后重复出现了4次的`Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9`。当时我脑子抽，完全没想到这是base64编码。。。

T_T...
