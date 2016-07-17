## REact (reverse, 250p)

[REact.apk](./REact.apk)

---------------------------------------

### 思路
这是一个用REact Native框架写的apk，REact Native是facebook开发的框架，基于这个框架可以使用javascript来编写应用逻辑。本来以为很难，但最后看到很有多队伍做出来了，也就看了下。用apktool解包后，在assets文件夹下有个用javascript写的代码，在里面搜索'alictf'，真的有。在网上格式化js[simplify.js](./simplify.js)后，看了下附近的逻辑，如下：

``` javascript
        {
            key: "handleSubmit",
            value: function(e) {
                var t = this,
                n = t.state.text;
                if (40 != n.length) o.NativeModules.MyBridge.show("Wrong, try again", 3.5);
                else {
                    var r = n.slice(7, 23),
                    i = n.slice(23, 39),
                    a = n.slice(0, 7);
                    "alictf{" != a || "}" != n.slice(39, 40) ? o.NativeModules.MyBridge.show("Wrong, try again", 3.5) : o.NativeModules.MyBridge.check1(r,
                    function() {
                        o.NativeModules.MyBridge.show("Wrong, try again", 3.5)
                    },
                    function() {
                        s(i,
                        function() {
                            t.setState({
                                text: "Congratulations! Reversing callbacks is fun"
                            })
                        },
                        function() {
                            o.NativeModules.MyBridge.show("Wrong, try again", 3.5)
                        })
                    })
                }
            }
```

逻辑很清晰，flag长度为40，格式为`alictf{`+16个字符的`r`+16个字符的`i`+`}`,`r`是用`Mybridge.check1`来验证的，很`jeb`反汇编下apk，很清楚看到check1的逻辑，用python反写下，就得到`r`的值，如下：

``` python
a = [ord(ch) for ch in 'excited']
b = [0x0e, 0x1d, 0x06, 0x19, ord('+'), 0x1c, 0x0b,
     0x10, 0x16, 0x04, ord('6'), 0x15, 0x0b, 0,
     ord(':'), 0x0b]

res = []
for i in range(16):
  ch = b[i] ^ a[i%len(a)]
  res.append(chr(ch))
print "".join(res)

# below is output:
# keep_young_and_s
```

接下来是对`i`的验证，我们看是用是`s`来验证的，往上找下，确实有个`s`，采用闭包，还有尾递归，但十分复杂。加上很多变量名是都是一样的，不好分析其逻辑。一开始问了下队友，是否可以简化这段代码（因为我不擅长javascript），但他们试了下，发现还是不行。最后还是只能慢慢看，发现关键验证在这里：
```
function t(e, t, r) {
    var a = e[c](l)[u](function(e) {
        return e[o][p](o)
    });  // python写法是 a = [ord(ch) for ch in e]
    ae(s, a,
    function(e) {
        console[d](e);     // d的值是闭包里的，为'log',所以这里是console.log(e);
        for (var s = o; s < e[n]; s++) if (e[s] != i[s]) {  //关键判断语句
            r();     // 错误时的回调函数
            break
        }
        s == e[n] && t()   // 正确时的回调函数
    })
}
```

看到这里，我们会去看`ae`的定义，然后跟踪下，但这里涉及太多递归，很容易看晕，所以决定采用动态调试。一开始我是firefox浏览器来调试的，下断点，看到一些关键变量的值。但发现貌似递归太多了，F8继续运行貌似有点问题，没有断点也断下来。后来采用打log方式，在几个关键位置写上`console.log`打印相关信息[test.html](./test.html)，运行后，查看log[test.log](./test.log),推理其加密方式，发现这其实是个矩阵乘法，这里还有个坑，结果是倒序存放的。用z3库很快就解出来矩阵了，详细代码请看[ans.py](./ans.py)

### 总结
虽然这题是熬夜做的，但还是挺值得的，当时好兴奋，换了几种方式，最后采用打log的方式成功推理出加密逻辑，解决问题的感觉真好！赛后和队友讨论下，这种js代码应该是AST工具变换生成出来的，不知道是否有逆向工具？现在也想知道别人是怎么做的，是否有更加快捷方便的方式。
