## debug (reverse, 200p)

[debug.zip](./debug.zip)

---------------------------------------

### 思路
这题使用了调试器的一些知识，启动程序后，创建一个新的进程，原来进程为调试器，新进程为被调试进程。使用`CreateMutexA`来区分调试器和被调试进程的逻辑。用IDA F5分析，调试器逻辑如下：
```
DWORD sub_4014D0()
{
  HMODULE v0; // eax@1
  DWORD v1; // eax@2
  DWORD result; // eax@2
  unsigned int v3; // eax@7
  signed int v4; // eax@11
  DWORD v5; // eax@16
  struct _PROCESS_INFORMATION ProcessInformation; // [sp+10h] [bp-4A4h]@1
  unsigned __int8 Buffer; // [sp+20h] [bp-494h]@1
  unsigned __int8 v8; // [sp+21h] [bp-493h]@1
  __int16 v9; // [sp+3Dh] [bp-477h]@1
  char v10; // [sp+3Fh] [bp-475h]@1
  struct _DEBUG_EVENT DebugEvent; // [sp+40h] [bp-474h]@1
  struct _STARTUPINFOA StartupInfo; // [sp+A0h] [bp-414h]@1
  CHAR Filename; // [sp+E4h] [bp-3D0h]@1
  char v14; // [sp+E5h] [bp-3CFh]@1
  __int16 v15; // [sp+1E5h] [bp-2CFh]@1
  char v16; // [sp+1E7h] [bp-2CDh]@1
  CONTEXT Context; // [sp+1E8h] [bp-2CCh]@1

  Filename = 0;
  memset(&v14, 0, 0x100u);
  v15 = 0;
  v16 = 0;
  StartupInfo.cb = 68;
  memset(&StartupInfo.lpReserved, 0, 0x40u);
  ProcessInformation.hThread = 0;
  ProcessInformation.dwProcessId = 0;
  DebugEvent.dwDebugEventCode = 0;
  memset(&DebugEvent.dwProcessId, 0, 0x5Cu);
  Context.ContextFlags = 0;
  ProcessInformation.dwThreadId = 0;
  memset(&Context.Dr0, 0, 0x2C8u);
  Buffer = 0;
  memset(&v8, 0, 0x1Cu);
  v9 = 0;
  ProcessInformation.hProcess = 0;
  v10 = 0;
  v0 = GetModuleHandleA(0);
  GetModuleFileNameA(v0, &Filename, 0x104u);
  if ( CreateProcessA(0, &Filename, 0, 0, 0, 3u, 0, 0, &StartupInfo, &ProcessInformation) )
  {
    while ( 1 )
    {
      memset(&DebugEvent, 0, sizeof(DebugEvent));
      if ( !WaitForDebugEvent(&DebugEvent, 0xFFFFFFFF) )
        break;
      result = DebugEvent.dwDebugEventCode;
      if ( DebugEvent.dwDebugEventCode == 1 )
      {
        if ( DebugEvent.u.Exception.ExceptionRecord.ExceptionCode == STATUS_ILLEGAL_INSTRUCTION )
        {
          if ( DebugEvent.u.Exception.ExceptionRecord.ExceptionAddress == &loc_4014A6 )
          {
            ReadProcessMemory(ProcessInformation.hProcess, &loc_4014A8, &Buffer, 4u, 0);
            v3 = 0;
            do
              *(&Buffer + v3++) ^= 0x7Fu;
            while ( v3 < 4 );
            WriteProcessMemory(ProcessInformation.hProcess, &loc_4014A8, &Buffer, 4u, 0);
            Context.ContextFlags = 65543;
            GetThreadContext(ProcessInformation.hThread, &Context);
            Context.Eip += 2;                   // 跳过无效指令
            SetThreadContext(ProcessInformation.hThread, &Context);
          }
          else if ( DebugEvent.u.Exception.ExceptionRecord.ExceptionAddress == &loc_4014B9 )
          {
            v4 = 0;
            do
              *((_BYTE *)&dword_407040 + v4++) ^= 0x31u;
            while ( v4 < 16 );
            WriteProcessMemory(ProcessInformation.hProcess, &dword_407040, &dword_407040, 0x10u, 0);
            Buffer = 0xE8u;
            v8 = 0xB2u;                        // v8 = Buffer+1
            WriteProcessMemory(ProcessInformation.hProcess, &loc_4014B9, &Buffer, 2u, 0);
          }
        }
      }
      else if ( DebugEvent.dwDebugEventCode == 5 )
      {
        return result;
      }
      ContinueDebugEvent(DebugEvent.dwProcessId, DebugEvent.dwThreadId, 0x10002u);
    }
    v5 = GetLastError();
    result = printf(aWaitfordebugev, v5);
  }
  else
  {
    v1 = GetLastError();
    result = printf(aCreateprocessF, v1);
  }
  return result;
}
```

可以看到主要是被调试程序异常报错后把信息返回给调试器，调试器Patch其内存并使之继续执行。有三处地方需要patch，我们才可以看到真正的被调试进程的代码。使用以下idapython脚本进行patch：

```python
from idaapi import *

def patch(addr, size, magic):
    for i in range(size):
        ch = Byte(addr + i)
        ch = ch ^ magic
        PatchByte(addr + i, ch)

patch(0x004014A8, 4, 0x7f)
patch(0x00407040, 16, 0x31)

addr = 0x004014B9
PatchByte(addr, 0xe8)
PatchByte(addr+1, 0xb2)
```

之后找到flag的主逻辑如下：
```
int sub_401370()
{
  signed int v0; // eax@1
  signed int v1; // esi@3
  signed int index; // ecx@7
  char v3; // al@8
  char v5[4]; // [sp+0h] [bp-10h]@1
  int v6; // [sp+4h] [bp-Ch]@1
  int v7; // [sp+8h] [bp-8h]@1
  int v8; // [sp+Ch] [bp-4h]@1

  strcpy(v5, "\x14R1");                         // 0x315214
  v6 = dword_40705C;
  v8 = dword_407064;
  v7 = dword_407060;
  v0 = 0;
  do
  {
    v5[v0] ^= 0x31u;                            // %c
    ++v0;
  }
  while ( v0 < 3 );
  v1 = 0;
  do
    printf(v5, *((_BYTE *)&v6 + v1++) ^ 0x31);  // Input Flag:
  while ( v1 < 11 );
  gets(flag);
  if ( strlen(flag) != 32 )                     // length is 32
    exit(0);
  index = 0;
  do
  {
    v3 = flag[index];
    if ( v3 < '0' || v3 > 'z' || v3 > '9' && v3 < 'a' )// [a-z0-9]+
      exit(0);
    ++index;
  }
  while ( index < 32 );
  sub_401290();                                 // 高低位换
  sub_4010C0();
  sub_401100();                                 // 高低位换
  encode_TEA(&tmp0, &AAA0);                     // TEA加密
  encode_TEA(&tmp2, &AAA0);
  sub_4011E0();
  return my_good();                             // 比较验证，输出结果
}
```

首先是解密提示语句（Input Flag:），之后判断输入的flag长度（必须为32），再判断是否为有效字符（[a-z0-9]）。
接下来是做一些变换，然后进行128轮的TEA加密，判断是目标值是否相同，如果一致即可。解密脚本请看[ans.py](./ans.py), 详细分析过程请看IDA的分析文件[debug.idb](./debug.idb)。

### 总结
1. 用搜索引擎对`0x61C88647`进行搜索，可以快速知道这是TEA加密算法
2. 用python写TEA解密算法时，发现一个问题，用`c_uint`可以得到正确结果，用`c_int`不能。现在猜测是最后结果在转换为正整数的时候（c_int & 0xffffffff）有点问题。


