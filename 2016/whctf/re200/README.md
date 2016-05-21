## Crackme_6 (reverse, 200p)

我讨厌数学
分值：200分 
数学没学好，你能帮我解出这道题么？

[Crackme_6](./Crackme_6.exe)

---------------------------------------

### 思路
这题逆向方面很简单，放到IDA里一看就明白逻辑了，如下：
``` c
int main()
{
  int v1; // [sp+14h] [bp-Ch]@1
  signed int k; // [sp+18h] [bp-8h]@9
  signed int i; // [sp+1Ch] [bp-4h]@1
  signed int j; // [sp+1Ch] [bp-4h]@8

  __main();
  v1 = 0;
  gets(flag);
  for ( i = 0; i <= 35; ++i )
  {
    if ( !flag[i] )
    {
      flag[i] = 1;
      ++v1;
    }
  }
  if ( v1 != 9 )                                // flag长度为27
    exit(0);
  convert(a);                                   // 转换为6*6的矩阵a
  Transposition(a);                             // a矩阵翻转为矩阵b
  Multi(a, b);                                  // 矩阵a*b = c
  for ( j = 0; j <= 5; ++j )
  {
    for ( k = 0; k <= 5; ++k )
    {
      if ( c[0][k + 6 * j] != d[0][k + 6 * j] )
        exit(0);
    }
  }
  printf("congratulations!you have gottern the flag!");
  return 0;
}
```
输入的flag长度为27，加上9个1，形成一个6*6的矩阵a。矩阵翻转90度为矩阵b。矩阵a乘以矩阵b得到目标矩阵。如果正常来做就是解多元方程式，比较复杂。但我们借助`Z3库`,可以很方便解出来，详细请看[ans.py](./ans.py)


### 总结
1. 条件约束问题利用Z3库来解决十分快捷方便
2. `BitVec`的位数对计算过程的中间量有影响，一开始都是char类型的，设置为8个bit，结果答案不对，因为这样算出来的答案是以8个bit的大小为限制得到的。所以最后设置为32个bit。虽然花费的时间长一点（位数大，花费的时间多），但保证答案正确。
