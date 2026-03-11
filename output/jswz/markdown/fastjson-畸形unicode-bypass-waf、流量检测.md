---
title: "FastJson 畸形Unicode bypass waf、流量检测"
source: https://mrxn.net/jswz/fastjson-bypass-waf-tips.html
asset_dir: assets/fastjson-畸形unicode-bypass-waf、流量检测
---

# FastJson 畸形Unicode bypass waf、流量检测

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/28 18:38
- 1613浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

unicode

waf

parser

---

# 前言

这事我在RainSec公众号上看到的，感觉是个比较新的姿势，特分享给我的读者。

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

这里使用 `Integer.parseInt` 把 `\u` 后的四个字符转为 `int` 类型，在 `parseInt` 方法中对字符串的第一个字符有特殊的处理，若字符串的第一个字符小于 '0'，则可能是 '+' 或者 '-'，关键点在于第一个字符是 '+' 时，则将索引 i 加 1，跳过该字符，同时不对转换结果造成影响.

网络安全

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

深入探索

Windows安全工具

文本剥离工具

SQL注入检测工具

这样我们就可以构造payload

计算机科学

```
{"\u+040\u+074\u+079\u+070\u+065":"java.lang.AutoCloseabl\u+065"}
```

这样的畸形unicode可以绕过几乎目前市面上大部分waf，另外我们可以注意到在第一个字符是 '-'时虽然也会跳过字符，但是在后续的代码中返回值是一个负数，如果我们有五个字符那么可以构造 `\u-ffbf`（转成int 是65，字符串为A），但是fastjson限制了读取4个字符，我们没办法构造出想要的字符串。

# 参考

- `https://mp.weixin.qq.com/s/7c_zi5Pv4a69IV0zzJo5Ww`

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#Java](https://mrxn.net/tag/Java)
- [#绕过](https://mrxn.net/tag/%E7%BB%95%E8%BF%87)

---

文章目录

- [1.前言](#toc-1-)
- [2.正文](#toc-2-)
- [3.参考](#toc-3-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKmElEQVR4Aeybi3rjuA6D+8/7v/OewBhIjCU7aXqJz676lQUNgLQqWmnT2f3z8fHxz1fjn91H7RdpxkUTRle+jzOtes980SrW2uTRc10xWsXolftKroHc6tfnVXagDeQ26Y/PxNk3UPvMfMAHcCelBtg04E7XBXCoSZ8FuCb9Z57KxQeuA5ocrWITS1L1Z/JS+tEGUsmVv28HhoEA7SmEMX9mqdDrnvHLA66pT5R4RTjlCbA/18KZLxzYn2uhao5CegJcCyMe1YuH0Q+dk2cfw0D2hnX9uzuwBvK7+/3wbr82kBz/io9WBz7e8c1qwR7oGP8jhF4Dzh/VRM9acv1d+GsD+a4F/9v7fOtAwE9Znh4hmHu0kfIqwH6g/RoO5moPeRWPOBhra80+h8/59/Vfvf7WgbTFrOTlHVgDeXnrfqZwGIheBs7ibBmpq54ZB35ZgI61JjlYTw/wNXSMVwjmlSdSGwR7oL8kRquY+q9g7TfLZ72HgcxMi/u9HWgDgf7kwON8tkRwXdVg5KLXpwbsq1x8M4yvauHAvYAmA9tfIOIRgrlmuiUwcjd6+1RNAo59YA2ew6353y9tIH+vF7x5B9ZA3jyA/e3/5Ah+BfdNoR/Vvabr3Ev5Twd4Lbkn+Br6D3U457JGGH3R0v+ruE5IdvQiOAwE+lMAzmdrBWvQMb76lISrCK6pXGrOuHiE8SlPgPvmWhgfWMu1EMzJlwBz0p8JsB86pg5GLtoRDgM5Ml6A/08s4Q94ivlu86QIw4E90FH6UaROGI/yRDjo/eBxnvqK0OvCQ+dyr2gVn9HiEdZa8D0qlxwea0Ds26/jwIbrhLRtuUayBnKNObRVnA5Ex1TR3LdE1wrwEQNurD+B7dj56vgrjD71fBSzjrUmeuXA9woXjxCsKU/EB9aASO2fA+IRRlSeOOOiCYFtv1InPB2Iilb87g60N4a5LXhqQKi7JyOkppkA7iYdjxCsKT8LOPaBNeiYXtC5rCeaMBzYJy6x14BId98zsH1/TbwlYG7WI9zNNnxGqwjuBaz/LuvjYh/rJevqA6lHKWuFfqRmXGqizRB6j5k/HHRf+kTLdcVoQnBt1ZNL3wfYX3kwBx2jw8jN+oN90YRgDkZMf+E6IdqtC8XpQMDT1OQScMzl+wJ7oP9FNfVCsB6/EMxJT4A56YrwQl3vQ7yi8nDfo2ryKh5x4B7yJmqNcrAH+vcs/izSC3rt6UDOmi3tZ3ZgDeRn9vXlrsMfF2un2ZGacakBH71cVwRrMD/Ss7577qgfuHfVn8nhtbpHvcF9oWNq8j0Jw1VcJ6TuxgXy9k4d+jThPq/rBGua8D7iqzyMfjAXf8VaW3nl4Drop2zmh+5TnQI6B85TC74GZN0iWkVge8cOHTfz7ktqKj3jwH2qb52QuhsXyNdALjCEuoThh3qOlrAa9zn4uAFNUo2iEQeJPPsAtpeDWUm8M61yMPZIbbD6k0cTwtgDRi61QdUmwr2C64S8smuPa152tIF8drrxC8FPEBhnqwFrMEf1UcCoz/rNONUrqgbuV7nkYA06ql4BIyd+H2BfegrBXPWKV4A1QJdbVF8byKasL2/fgeHX3tmK6gSjA9trPoy/gkLX4p/1iCYE1zzyyfuTAV7Ho3uAfVlv9YcDe6BjtIq1dp2QuhsXyNdALjCEuoQ2kBwh6MerGpPHVxF6DRDrIaa2GmZcdGB7eYxHGG2G0vcx84Wr3jMOvA4gtm1dwBRnfWH0tma3pA3klq/PC+zAywOBPun99zF7Mvae/TX0fuC89lG+rzm6BtcDR5aNV08F0J5wXSs2w98vYP3v5QbyKLaLgy/gOuDAYRpo9395IG61vn73DqyBfPeOfrHf6d+y0hv6kQqn45rYczD646mY+opVTw69HziPVhGs1X5gDoxVS23lwL5oRwj2pfbIFz6+itEqrhNSd+MCeXunnrWAJw+Emv5nlUD7QZSpt4JJAt0PzqsNzKWXMLpyRa6FYL/ys1BdDXAddKz18c64aBXje8SB7xd/xVq7TkjdmQvkayAXGEJdQhsI+EjV4xMjWANC3b2MhQS2l7Ha4ywH+4G0uENg6xdy1iuaMDq4DkaMpyKMPvU7CxhrwFx6g6+Bs1Z3WhvIHbsu3rYDw0CA7akE2qIycWFIoPnAuXRFPBXBHqDR8u4DaH2jtYKSQPeB88ipE4YLgr1AqLvTrhoF0NYRI3ROnqMA+2Y6WAPS9g6Hgdyp6+LXd6C9Mcw0n11B/BWB7amqPcBc9UUHa0CoOwTu+oGvof+jWC2AroPzel/lj/xVTw7ulWshmIMRdR+FfAmwL9cVwRrwjv+D6mN9nOzAesk62Zx3SG0g4GMzWwRYA5oMbC8nQON0TBWNOEiArbbKYE71+4iv8mdctIpw3L/2BftqbfTK7fN4hDD2iF96IlzFNpBKrvx9O9D+lpWpVTxb1swHfjKg46xHrd3n1Q+9D9zn1Zd830vXew16n2gzVG1ipoebeWZc/BXjq7hOSN2hC+RrIBcYQl3C6UDqUUqeYuhHH5xHi1cYDuyBjtEqwqirj+LIB66p+j4He9QnAeagY7RaD9Yrlxwea0DsUwS2X3KA9T7k42IfpycE+uTAeZ6gGeZ7A3uhv6Ou/pkPXFN9ycFa6o4QRh+MXOrTv2K0R1hrlFc/+J7i9wHWgFZSPacDaRX/B8m/ZYlrIBebZPvj4tm66pGKD2g/iMJVX/JoFaNVjA6f6zvrkV7C6MoVMPYX/0yklzB+6P3AuXRFPEKwpvws1gk52503aO2deu4NniT0H8jRhGBdT0BC/KMA18EcU5+ewnBB6LXhKqpGUTlwjXjFTAN7YI61Zp+rp6LyMPapenIYfeuEZHcugmsgFxlEltEGAj4+On6JmMAaEKr9QAeGvJluCVi/pcNn7lOxmuC+9siXGrj3i08NjJr0VwPcD4yv9lFd1ihsA5Gw4v070Aai6ShmSxL/TKQW/NTA/BeD9Ir/EYL7Vd9ZD7AfOsb/Cua+0PuFO+sXj3DmE6+A3rcNRMKK/Q78/nV7Ywh9SvC5fL/s+jTstaNr8D1nevqBPUCzAe1nWCNPEuh+cD6zgzWYn/J9DXT/Xnt0ne9PuE7Io936ZX0N5Jc3/NHt2kB0XD4Ts8aph/H4RhOmFkZfNKG8CrBPeUK6ItcVxX8mwP2BVlb7AdvLYuWa8W9ypv21DJCaKrSBVHLl79uBYSDgpwHm+MxSM3khuM+sTvo+wH7oGM+sx4yLv2J8lUse7RWEvk64z2s/uNeAJgPbCQTWP+F+XOxjOCEXW99/bjnfOhDoRw+c52UBfA20TQbaUQ0Zf8Vo0P3wWp5eQnAP5QkYub0G/b1JXec+T13F6oHxXt86kHrjlR/vwJnyIwN59BSAn4yZD6wBbd3AdpIaUZLaI3mRWzrTwlVsBSWJXqjTFLze1AlTANagn7Jowh8ZiBqveG0H1kBe27cfqxoGouN1FmcrSR30Y3nmr1pqK5d8ps24vV+ecNDXBMd5/BXBfvVLgDkYceZJv2hCcK3yxDCQFC58zw60gYCnBc/h2XIz7YrVH75ysxy8lpkWDuwBQk0x93wWp00mZPpNpOn/bj3zVa4NpJIrf98OrIG8b++nd/4fAAAA///Y+U1MAAAABklEQVQDABle3GsKvEICAAAAAElFTkSuQmCC)

手机扫码阅读
