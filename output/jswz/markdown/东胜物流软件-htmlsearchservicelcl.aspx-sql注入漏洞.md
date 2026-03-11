---
title: "东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html
asset_dir: assets/东胜物流软件-htmlsearchservicelcl.aspx-sql注入漏洞
---

# 东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/17 08:45
- 200浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

木马

服务器

身份验证

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 HtmlSearchServiceLCL.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `HtmlSearchServiceLCL.aspx` 的代码引用 `DSWeb.PriceCarrier.HtmlSearchServiceLCL`，在dll中找到它的逻辑实现

深入探索

Nessus

在线安全工具

Web安全课程

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-001-769087f56a45.webp)](https://image.mrxn.net/d47e42726bb441e9ac07f35052466179.webp)

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-002-c9855c0dbef5.webp)](https://image.mrxn.net/7a54ee092a18499c873b0485abb6ba5b.webp)

关键点如下

SQL注入检测工具

深入探索

SQL

数据库

鉴权

```
// 接收未经验证的排序参数
if (this.Request.QueryString["sidx"] != null)
  this.strSidx = this.Request.QueryString["sidx"].ToString();
if (this.Request.QueryString["sord"] != null)
  this.strSord = this.Request.QueryString["sord"].ToString();

// ... 在 GetSearchSeaPrice 方法中 ...

// 直接将用户输入拼接到 ORDER BY 子句
strSql = string.Format($" SELECT ... FROM eb_pricequery WHERE ... ORDER BY {this.strSidx} {this.strSord} ", ...);

// 执行恶意的 SQL 语句
DataTable table = ebPricequeryDa.GetExcuteSql(strSql).Tables[0];

//---------------------------------------------------------

// 接收未经验证的搜索参数
if (this.Request.QueryString["searchString"] != null)
{
  this.strSearchString = Regex.Unescape(this.Request.QueryString["searchString"].ToString());
}

// ... 在 GetSearchSeaPrice 方法中，对 searchString 进行解析 ...

// 直接将解析出的值拼接到 WHERE 子句
string[] strArray3 = strArray1[index].Split(':');
...
str1 += $" AND CARRIER = '{strArray3[1].Replace("\"", "").Replace("##", ",")}' ";
...

// 将包含注入的 WHERE 子句拼接到主查询
strSql = string.Format($" SELECT ... FROM eb_pricequery WHERE TYPE='LCL' {str1}{this.strSearchOper}  ORDER BY ... ", ...);

// 执行恶意的 SQL 语句
DataTable table = ebPricequeryDa.GetExcuteSql(strSql).Tables[0];
```

可以看到通过直接拼接用户控制的请求参数来构造SQL查询语句，导致查询功能中存在多处[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /PriceCarrier/HtmlSearchServiceLCL.aspx?page=1&rows=10&sidx=SQLI_POC&sord=asc&searchField=&searchString=&searchOper= HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-003-ac6e2a69e262.webp)](https://image.mrxn.net/92bc0c9b70c8480c90ccc804603527e3.webp)

成功延时 5 秒

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK10lEQVR4Aeya0XbbOAxEfff//7lbBL0KORItO01jP2hP0eEMBiBDSCdxuv/dbrdfX4lf8V/2ML3SzYv65KK6mLr8CLNGz0o3L6Yv+ZlP/zNYA/ntv/68yw1sA/k97dsjsTp41gI3YLObBz50aNwMfxYw69aJf2wbQPthj1kD7bEYmkNj6tZD55ND69Yl6j/DsW4byChe69fdwG4g0FOHGc+OCLM/n4qzev36YO4HM9c3oj3EMTeuzSeOnlpD71nrCmhuXWmPBHQdzHhUuxvIkenSfu4Gvn0gPj1w/DSYF/NLTf1RXr7sBcdngFmH5ln/KK+9Kx713/N9+0DubXblzm/grwcCx09XPTEVeQRoPzSah+bQWLUV5mtdAZ1Xh+awRz1i1VckL60CuketK/StsDwVq/xX9L8eyFc2vWrWN7AbSE38KFYt0vvh+/0X9NP2ezn90a8Ixz7zK7TPEVpjTn6G6ZeL1sNzZ7Y+0X4j7gYyJq/1z9/ANhDoqcN9zCNC+9WhuU+DugjH+TO/9YnQ/YBMPcyBj98eWADH/NkzQveB++i+hdtAilzx+hv4z6k/i48e3b7QT4n8q/VZZ7/CzEHvmbocOl+1Feq1roA5DzNPf/Lq8Wxcb4i3+Ca4Gwj0UwCNeU5oHRrNw8zPdPMidL1PFDSHRvX0Q+fhE/Wsas7y0L30QfOzftA+aMx6+T3cDeSe+cr9+xv4D+Zprp4CaJ95MY94pkP3gcasX3Fo/6r/WKcHumbMjWuY89atEI79Y89xDe23HzQfPbm+3pC8kRfz7acsOJ6e0/Wc0D5oVNcHrUOjevpWOnSdfvHXr18f/6KZ3D6F5sTSKpKXVqEuQu8NjalXTUXqMPvLU6EvEWb/mL/ekPE23mC9+x6yOlNNfAx9atBTl5uH1mFG8+mXJ+oXYe4HfLxBVQed07vC8lbA7C+tYlX3rA5zf+thr19viLfzJrgbCPTU6gmp8JzQOjRWrsJ8rSvkYmlHYR66X3KY9czLx97QNWowc2tE6LzcOnkizP7MZ71cPPNXfjeQEq943Q08PRCnDf20wDHq80uD2aee+GwdfPbNWntDe+SifhFmHzQ3bx3MeubTJ0+E7gOf+PRAsunFv/cGts8htnXa0FNTF6F1feqiOrQPGtX1waxDc/OideJKr7w5mHtVrgJmHZpDo/WJMOerV0X65ND+8lSo13qMI/16Q7yVN8HTzyHQ0/a8Thhm3fwZWp8+dTjuC63rsx5ah09Mj97UP/ivX9vnF31i5uXm4XNP+FyvfNaJ+uCz9npDvJ03we17SE7L86mL0NM0nwid1y9C6ys/dF6/CK1bBzPXN6JeNXkizL0ynxzaD432T7QO2icXoXVoVC+83pC6hTeK3feQs2mbz69BXVzlU08O81Oz6mcdtB9Q+vg/SGDNN+OfBfBR417QHBr/2DZInwmY/frMi+qieuH1htQtvFFsA4F5utAcGj0zzDx1mPMwc/1HT0fl1GGuUy9PBcz50gy90J7k+lao3zx0H3kidP6sDtpnPcy89G0gRa54/Q1sA3G6ME9NPdGjpy6H7iPXD61DY+b1qUP7oFFd34jQnlE7WsPsy55wP3/UszSY60qryP6lrWIbyMpw6T97Aw8PBHr60OjUoTnMmHm/LHU5dF1ymPXMZ5/Kq0HXyitXccbLcy+sh7m/uni73T7aJP8QT/56eCAnfa70N93A9kkdeuqrvk5b1CcX1RPhsf7WnfXTd4TWQu8JjUfeI816czDXZz59MPvNZ518xOsN8bbeBLdP6k4pzwU9bXgMs49ctL9cVBeh95Mnwj4PrUHjqib3hNkPzfWJq37Q/rM8HPvGuusNGW/jDda77yGrp0E9Mb8GuP8UwHEeWj/r737pG7ke0Zwcei9oNA8zX/mhfeZF+ySaF6HrYY/XG+ItvQnuvodAT80p5zmh86k/68/65DDvc9YfyBbbvwQC029zsxd03gbQHBrVs049EeY681kvH/F6Q7ytN8FrIG8yCI+xG4ivD3Cr0Cial4vlrci8vHIV+sXSKvSpJ1dP1FeYOXnlKmqfitQrV5H6in9Vr70raq+KWmfsBuJmF77mBnY/9q6OkZOUn/nN1xMxRuryVd/U5UeYvfS4v3nxLJ8+eaJ9Elc+zzPi9Ybkbb2YPzyQcYrjOs/v06FHLqZ/xfXbR1z5n9HtnTUrXd+jZ0ifPNH9Rnx4IB7qwn97A9tAnJ7bJR+nOK71i1mXurXqZ3jmd79Ce9W6Inn2Sq5frB4V8pW/PBXpK61CXVz1qfw2kCJXvP4Gtl+d3JvaeMyaeMWo1bq0irM+5amomjFWdeWtGL3j2rrC8lWM+VpXrqLWR1E1FebKO4Z6ecZQF83JE+2ZunWF1xuSt/Nivn0OyXPkNGt6Feq1HkPdPsnVb7evrVb9xjPYWe+Yq7X5WlfI06++Qv0rXNXVnmPoG/tcb4i38ia4HIiTzHOqO9XMy/WJ6U9unWhd8tTtM6IeNXs8itaL1tkvdfOp60/UL1pXuByI5gt/9ga2n7Lc9mya5muaFdaJpVXoE82L5alIXlrFqk69PKtIz4rn3vJH0f31u4888+qieesKrzfE23kT3AbitBLznOZrmhWZL61Cn/nk5TkK/WJ6so++Qr21rkhe2jNhvZi16qszZX7lUy/cBpKbXfw1N7ANxGmujmFerGlWJC+t4qyP+fKOoS6ak7tf8tLTm7w8FepiaRXZU65PXt4K9VpXyBOzTn6E20COkpf28zewG0hNeow8ktNPXW6t/KuY+yS3r3rhau/KjWHtym/emhW3Xp9cf/KVrq9wNxCLLnzNDSx/l+XU81g1xYozvTwV6bOvmPmqqUhdbl15MsyJ1qRPXUy/+qou/fpSl6/y7jPi9YaMt/EG690n9dWZnLaoT36G+kWfGrlon8zLRf0jZk5uT73qydX1iyufuj7r1c/wyH+9IWe39sP53fcQp+055E5TNL/i6qL+RzH3faTOmvR6hlV+pdsn83JRX6L7pp7cPoXXG5K382K+G4hTFT1fTW+MzMv1ZJ38q2jfxLGfZxi1o3X2sE5dflRb2lm+PBX2E0urSF6asRuIiQtfcwPLn7JWU8ynQ5/olyFPf3L9K90+6Vv5y3cvN+bPfLdbuT/Ds4hmso/8DK0f8XpDxtt4g/X2U5ZTF1dnMy/6FOhPrp5ovXrysz76j9CeK8wafe5pXi6mL3XrEq1L1GefwusNyVt6Md++h9R0nok8t7VO3XxyddE6Uf1RtK4wa9xbzLx8lT/TV/k6S4X9E60rT8WYv96Q8TbeYL0NxKmdYZ45/TXxo7BOvx518VndfoX2EFe9zvLWiWd+82KdpUL+DG4Deabo8v67G9gNxKci8dEj1JNxFNbbV65Xnph+8+pHqEfUkzz3lov65WL206eeaP4R3A3kkaLL8+9u4K8H4tPgEeWiemI+bfLEVV36Rm7NqNVaPdGzipmXm69eFclLOwrrza146X89kGpyxffdwLcPxKdA9ClaHflZn33O+pZPT2LljuLsLOatTa4uuq98hfYp/PaBrDa99MduYDeQmtJRrNrp9WkQ9Wdebv4M05/95SNmz+yRXL895PpSX/HU7ZN4z7cbSBZf/GdvYBuIUzvDs+PlU2W/rFMXM588fe4z+tTEMTeu7SXqF/WaX3F1MevVxVU/9cJtIBZd+NobuAby2vvf7f4/AAAA///JII0SAAAABklEQVQDAFR/Wdfebn2cAAAAAElFTkSuQmCC)

手机扫码阅读
