---
title: "金和OA GovDel.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GovDel-sqli.html
asset_dir: assets/金和oa-govdel.aspx-sql注入漏洞
---

# 金和OA GovDel.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/17 13:31
- 226浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

SQL注入检测工具

网络安全培训

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GovDel.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GovDel.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.govsetaip.dll` 将其进行反编译后找到 **GovDel** 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    string strID = string.Empty;
    if (this.Request["strId"] != null)
      strID = this.Request["strId"].ToString().Trim();
    this.getPaperName(strID);
  }

  private void getPaperName(string strID)
  {
    DataTable delPaperName = JHSoft.GovsetAip.DelPaper.getDelPaperName(strID);
```

跟进`getDelPaperName`方法

```
public static DataTable getDelPaperName(string strid)
{
  string str = $"select SysF_Id,SysF_Name,SysFile_Type from GovPaperAip where SysF_Id in ({strid})";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

参数`strId`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govsetaip/GovDel.aspx/?strId=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GovDel.aspx SQL注入漏洞](images/img-001-ff2c52ba57d9.webp)](https://image.mrxn.net/5d455e883a7d44f1bded241fb5120b19.webp)

成功延时 4 秒

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKHUlEQVR4AeyajZbjtg6D5+v7v3PvIiwkRqIVpzsT+27VUxYUAFKOaM3f6V9fX19//278feKfao9cZv0VZ73yW8u48lmr8GwP+6oe/4bTQH7V7X/vcgJtIL8m/fVOVB8A+AKeJGDibIDQAFMlAj/SY/V5qweBeA6gkhu36ltprfBX0gbyK9//3uAEpoEAj7cRalw9s6efPRWX9TGHvq9rjaN3XEPUZn6shfAAzQa0z2wSZs69hPatEHoPmPOqdhpIZdrc505gD+RzZ31qpx8ZCKyvp678GH7azJuD436V33VCiFrliuyHZ006zJxrpP90/MhAfvqh/+T+Pz4Qv10Z4fgthNCg49kBeI/sN2eEdV/7co9P5j8zkE9+gj9srz2Qmw10Goiv7BGunh/iy0GurfzWIfzQ0VrGqoc56LUrzlruW+WVzxz0vSByaxVW/TNX1UwDqUyb+9wJtIFATBzO4dlHhOiX/RDcq7cFnn25h2szt8ohemUPvMd5T2HuM+YQfeEc5vo2kEzu/LoT2AO57uzLnf/S9fvdKDv/Q7r3P8sHmIN+pc09DAf/sUcIUavcAcHlcnjmINZAswHtj4tjL2Dps+i638V9Q3yiN8FTAwHaGwTHud8OOPYA7aPbLzQJtL3MnUX1UZz126cah7mM1jJCPKd9EGvoaO0IIbxZPzWQXHBh/p/Y+i+IKcGMqxPIb4t9ED0qreIg/IBblAg8bk0W3Q9CA7I85fZXCDz6Q8epwUC4z0A/LaH3g8izoeqxb0g+oRvkeyA3GEJ+hOnH3ixWua8ZxBUE2v+tYj90bcVZy+j+Ga3D3Df7IPTMOV/1sPYOQuwFgbnWe1aYfRC10HHfkHxCN8jbQCCmlJ8JgsuThmPOtdlf5ZXP3HcgxDMCp9qtnjE3ANo3f/Ou9foIIWqPdPNtICY2XnsCeyDXnv+0e/s9ZFIOCF9RiCsI/Zu6taoUur/SzcGxz/2F0H0QuXtkhGdNtQ4IDWbMPZy7TmjOKM4B0c+a0JryVewbsjqdC7Tpx15PUujngZg4dJTusK9CiBp7hfZBaICp9iO0fMDjm6hFiDX0W2ntd1B7jVH1g3l/CO6V3zqEH+rPsG+IT+omuAdyk0H4Md4eiK829KvnZtA5iLzyQ2iuywihQb/S7pF9VW5fhRB9qzoIDajkx5dNqDUXAM3n/a1ltCbMvPO3B+LCjT9zAtOPvdAn7S01TQeE7rUQgrM/I4Qm3xiVL3POYe5hLfeE8FkTwjMHsYZ+A+VzQOheC72HcgeEz1pGmDXXVZhr9w2pTuhCbg/kwsOvtm6/h1Sir1KlQVxLmK++6zJWPV7prrHP6yNc+axlhPgMmTvqLT77nIs/ExB7ZS/M3L4h+YS+L//Xndo3dYhpefJCCA46eifpDnNG6H6I3JoQZs69MsqrgNkP5zjVKyD80NF7QefkHQNCH3mtITToKF4BnfNe4seA7ts3ZDydi9fT9xDo0/JUM/p5ofsg8uwbc9dlhKgDGg20X7AauUhg7fdzVC0gaivNdcJKh6iVrqg84h0QfuhoLdfuG5JP4wb5HsgNhpAfoQ3E1ycjxPXKBc6zz9wKIXoBpQ14fKmqRO+10uSpdIi+0hWV5xWnOgVEL1j/qL/qpz6OytcGUomb+/wJtB97q62rSZqD/ra4FoLzWgjBue4VqsYBUTuuAVMlAo/bBjQdeHDV/s30RgLRDwJzqfeA0GC+UfJD6PYL9w3Rydwo9kBuNAw9yvL3EIgrBTPqeh0FdL890DmYcz3MO+G+ucbcCrP/bA7xvFVf94DwQMfsty+jdeg1+4bkE7pBPg3EU8uYn9M89KnCc26PMNc6Fz+GtYz2mPNaCLGntVcI7/lzP+2nyBxEP/Fj2AfhAUw9frAAHtjIlEwDSdpOLziBPZALDn21ZRsIxDWCGfOVdLMVB71H5YeuQ+T2ZYTQIDBr3h9CA7LccuDpywPEGjq6V0boupvBmoPQ3cd1QghN+SraQFamrX3uBE79pg4xXaA9GfB486D+LbQZi6R6g2yzJhw56HtC5PZkhNBg/WzaQ5FrV7m8Dvu8zlhp5jJCPGfm9g3Jp3GDfPrF8NWkIaZa+SC06nNBaNCx6pFrrWdulUP0dp1w9ItzQPiho/32CM2tEHoPmHP1UeQeWisyd8ENydvvfDyBPZDxRC5eTwOB+bpB5/y80DmIXNdPYY8QQlPukEfhtRBmH8ycvArVK5Q7tFZA1EFH8QqYOdcLIXTl74R6O1zntXDFWRNOAxG547oTaAPRFBXVo4h3WPc6o7VXCPNb6D65duS8FmbfKpdXAbGncgfM3KhBeOAZvScE77XQPZQ7YPZZy9gGksmdX3cCeyDXnX25cxsIxJXydctYVUL4Ycbsd5/MVTnMfSC4ym/O/YUQfuUOCM7+jKMHyHLL7avQJqD95QIityZ0rXIHzL42EJs2XnsC7W9Z1QT9aBCThP63IfsrdF3G7Mu886yPOfT9IXLXZXTdKy7ryl0nhLk/BAczqmYM9VRA92s9xlin9R9zQ8YP+/+63gO52eSmPy5Cv2YQua6SA4KDGf3Z7BWayyheAXMP6FyuUa4ah9YKOPZnXfkYELUjP669Z0Z74FwPCB90HHsAX/uGfN3rn7cHkt+SMYc+fXjO88eG0Mb6cQ3PvqpH5pxD1AGmTqOfIRcAjx9pM1f5sn6Uu05Yed4eSNVkc993Ansg33eW39Kp/R4CcS11lcaA0IC2KfC4xtCxiSlxL+g+c8k29YL+Ow/0WojcPTLCsZb3GnOIOmCUntbA9Jw2QNfMvUKImuzbNySfxg3y9mOv37TqmawJrSsfo9Jgfgtg5sZeWlf9xCsgekBH8QrXCSF05QqINaDlFMDjFqiPwyavhRUnPoc9QvMQ/aF/BZDu2DfEJ1Hi58npewj0CcK5fPXYfjMqzHVwvJd90D3mcl9zGbM+5tk35tD3ch10buUftXfW+4a8c1of8O6BfOCQ39miDcTX8iyuNoF+tSHy7IfgoONqXwhf5cl9VzlED+ho/6u+EDX2V5h7VDpEj+yDmWsDqZps7vMnMA0EYmpQ45lHzG/BGf8rj/tVPujPaR1mzpp7Cc3B7JfusK9C6LXwnL/yW4deNw3Epo3XnMAeyDXnfrjrtw7EVxz6FfTOMHP2CyF0+4UQHMwofQwIn/o5ILjRq7U9yh0QfuhoX0b7M+e80sxlHP3SvnUgarjj9QmsHJcMxG8GzG9h9bD2Z4SozX7rFVdp2ed85YPYE7D98Xcv6GsJqx7WhMCjXjWOSwbizTfOJ7AHMp/Jpcw0EF2lVZx52lxf+WG+qjBzVa057+G1EKIHdBR/FBA+9xIeecVLd2h9FBB9s36mTv5pICJ3XHcCbSAQU4VzuHpk6D0q3+ptgV5rHwRX9cqc/RkhamFG+6Brud+Yw+xb9YDZDzPnHsI2kHHzvb7mBPZArjn3w13/BwAA//9i5MHpAAAABklEQVQDALLafLzAWpTEAAAAAElFTkSuQmCC)

手机扫码阅读
