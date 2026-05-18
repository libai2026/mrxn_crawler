---
title: "FastJson 畸形Unicode bypass waf、流量检测"
source: https://mrxn.net/jswz/fastjson-bypass-waf-tips.html
asset_dir: embedded-base64
---

# 前言

这事我在RainSec公众号上看到的，感觉是个比较新的姿势，特[分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB "标签：分享")给我的读者。

字体

# 正文

fastjson解析unicode 部分实现逻辑 com.alibaba.fastjson.parser.JSONLexerBase#scanString

```
case 'u':
    charu1=this.next();
    charu2=this.next();
    charu3=this.next();
    charu4=this.next();
    intval= Integer.parseInt(newString(newchar[]{u1, u2, u3, u4}), 16);
    this.putChar((char)val);
    continue;
```

深入探索

漏洞扫描服务

代码注入检测

原创内容授权

这里使用 `Integer.parseInt` 把 `\u` 后的四个字符转为 `int` 类型，在 `parseInt` 方法中对字符串的第一个字符有特殊的处理，若字符串的第一个字符小于 '0'，则可能是 '+' 或者 '-'，关键点在于第一个字符是 '+' 时，则将索引 i 加 1，跳过该字符，同时不对转换结果造成影响.

网络应用与在线工具

```
if (len > 0) {
            charfirstChar= s.charAt(0);
            if (firstChar < '0') { // Possible leading "+" or "-"
                if (firstChar == '-') {
                    negative = true;
                    limit = Integer.MIN_VALUE;
                } elseif (firstChar != '+')
                    throw NumberFormatException.forInputString(s);

                if (len == 1) // Cannot have lone "+" or "-"
                    throw NumberFormatException.forInputString(s);
                i++;
            }
            ...... 
}
```

这样我们就可以构造payload

```
{"\u+040\u+074\u+079\u+070\u+065":"java.lang.AutoCloseabl\u+065"}
```

这样的畸形unicode可以[绕过](https://mrxn.net/tag/%E7%BB%95%E8%BF%87 "标签：绕过")几乎目前市面上大部分waf，另外我们可以注意到在第一个字符是 '-'时虽然也会跳过字符，但是在后续的代码中返回值是一个负数，如果我们有五个字符那么可以构造 `\u-ffbf`（转成int 是65，字符串为A），但是fastjson限制了读取4个字符，我们没办法构造出想要的字符串。

# 参考

- `https://mp.weixin.qq.com/s/7c_zi5Pv4a69IV0zzJo5Ww`
