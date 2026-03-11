---
title: "孚盟云CRM AjaxAttachment.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html
asset_dir: assets/孚盟云crm-ajaxattachment.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxAttachment.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/15 16:46
- 664浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

鉴权

身份验证

漏洞预警服务

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxAttachment.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxAttachment.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxAttachment 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["method"].ToString();
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.empID = UserCookie.GetCookieValue("empId");
    this.empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.empID);
  }
  string str2 = str1;
  if (!string.op_Equality(str2, "AddMouldAttachFile"))
  {
    if (!string.op_Equality(str2, "saveAttach"))
    {
      if (!string.op_Equality(str2, "uploadFileToOss"))
        return;
      this.uploadFileToOss(context);
    }
    else
      this.saveAttach(context);
  }
  else
    this.AddMouldAttachFile(context);
}
```

当 method=saveAttach 时，进入saveAttach方法

```
private void saveAttach(HttpContext context)
{
  Helper.WriteLog("savePriceAttach进入方法", "products");
  try
  {
    UserCookie.GetCookieValue("corpId");
    string str1 = context.Request["FUIDs"] == null ? "" : context.Request["FUIDs"].ToString();
    string SQLString = $"SELECT A.*,B.DocExtDescrip AS FileTypeName,C.CNEmpName AS OwnerName,\n          D.CNEmpName AS KeyInName,E.CNEmpName AS NearEditEmpName \n          FROM dcFileMouldRelation F \n          JOIN dcFile A(nolock) ON F.FileFUID = A.FUID \n          LEFT JOIN dcDocType B(nolock) ON upper(A.FileType)=upper(B.DocExtSign) \n          LEFT JOIN bfEMP C(nolock) ON A.OwnerID=C.EmpID \n          LEFT JOIN bfEMP D(nolock) ON A.KeyInID=D.EmpID \n          LEFT JOIN bfEMP E(nolock) ON A.NearEditEmpID=E.EmpID \n          WHERE F.MouldID = '{(context.Request["MouldID"].ToString() == null ? "BF001" : context.Request["MouldID"].ToString())}'  and  A.FUID='{str1}'";
    if (((InternalDataCollectionBase) this.dbHelper.Query(SQLString).Tables[0].Rows).Count <= 0)
```

未经过滤或参数化绑定的参数 MouldID 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

Nessus

安全

文件大小转换

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxAttachment.ashx?method=saveAttach&MouldID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxAttachment.ashx SQL注入漏洞](images/img-001-5b285b2a2c7a.webp)](https://image.mrxn.net/113a076a70c04b90a45d2687c0082c9c.webp)

通过报错注入 成功在响应回显数据版本信息

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALYklEQVR4Aeyci5Ybtw4EVfn/f841treoIUTqYW8snXNnj+kaNBoYmhhFkfL453K5/Ps769/vH2u/wwH1zmHYXOg3bbyjviP1HrW6Vpel3Vv6OnuNeXXj32EN5Ffd+etTTmAM5Nd0L8+s3caBC1yXPnsad0Jq1Hd+9U7ripBeekqrBff18tSC+CAsbbUgeQhXntLcxyOW1zUGonDyvSdwMxDI1GHms9vsT0Ovg+f6Qnz2g8T2gzlWX3HXo3v1SfPGneYfEbJXmLmquxnIynRqf+8E/nggPjV9y5CnQb37eqxP7vKQvqv8Sqt+kJq6Pq5n/ZB6CI896nrXp3Kvrj8eyKs3PP33T+A/HwjkqYKwb+fR0wXrOogOj+k9pHuA1PZYX6c+ad74J/ifD+QnNvn/1ONmIE69c3cokKdM/5fv8Ju6NAWpM5Yw671On/qK3QNzT/M7wuyHxN4LEu/qu25dZ/dVfDOQEs/1vhMYA4FMHe7z0VYh9T4NkLjXPcrrh9TrV5eQPKD0NO0JfH3LYPx0g28jpP47HIDocJ+j4NfFGMiv6/PXB5zAPz4Vr7LvHfIUdN2+kLxx90Hy6pB459dnvqgmIT2MZXlrQfJ1Xcv8I5a3lr66rtXj0l5d5yvEU/wQ3gwE8tTATPcL0Y1lfxJg7YO1/rt9IP3gSntJ9wbxdN0Y5jwk7vUQvddBdJipT8Kch2t8MxCLTr7nBMZAIFPyadht51Ee7vexHmZf1yH5vg99sucr7jlIL3VIDDPNd1bP4zKv1uOdDrlf9xsXx0BscvK9JzAGUtOp5XbqupYxZLowszy1IHpd17JOllYLZh8k7r7yHtflcvmyQPwQfomb36w3DalRl+YlxAehun6YdZjjnU/dfhJSD1zGQC7nz0ecwD9wnQ5cr92dU92x+4whvZ6Ndz71Vwi5N4Tu3R4QHUL1HSE+CLuv9zevDus6fUeer5DjaXzA9c1AHk0V1tOGWX/Ux7zcnQWkL4T6rDvS3LO0Vj+s72FeWgfxQ6iuD2YdEkPY/VV3M5ASz/W+ExgDWU1rta2dTx0yfWvVdzHMfn3S+k7zK+pd5Urb5bsO9/dWvWpZB/FDqF6e4+q6cXEM5FhwXr/vBMa3vZCpQuiW4LXYOglzvbqsp6IWxFfXtcxDdOM/YfWtBXPP0mpB9Lo+Lu+pBvGpQ2LzEqLrUzeG5OHK8xXi6XwIx0CcXmffp3l1Y8iUjXteHeIzvyPMPrgfH/tAvN7THEQ3/uITv/U+PbYFzP31QXQI9Zs/cgxE08n3nsAYCMzTg8RODxLDzN32YfZB4p2/695X3Rge99Frbad5mHup64fkYaZ5aZ1Uh9SpS/MS4gPO77IuH/YzXiHuCzKtPk1jqV+qQ+rVpXmpDvGrQ2IIu24sIT7AljcEvv6tEhOQ2B5dN+7sfmNIPwh7HUSHmfrsU7wZiKaT7zmB8W2vt68p1YL1NCG6fpjjqq1lXkJ8EKpL+D297uV61Mv8zt91/RLmPcIcWw+zbr3sPogfON9DLh/2Mz6pP9oXZIpOd+eH+Mzrl+pSXXbdWEL664fEgJanCXy9t6x6ATf/zaWNYa5Tf0Tvo8/4yPM9xNP5EI73EKcE96cP6zxE738uiA6h99EH0SE0D4n1dcJt3truNd7lYe6lD6JDaB8Ja/1yuWj5ov2+gl+/Qeog/CWNX+crZBzFZ1yMgcDttFZb7NM27uy15tUh91OX5uUrOsw9YR333t5DPsrr64Tcr9cby16nXhwDqeBc7z+BMRCn9mhLkKcAZloH0Y3tC9EhVNcnIXnjHWHvgzkHiXf39B4QH8w0L2HOQ2LzEqJDqC4hOlw5BqLp5HtPYHwOgUxptx2frk79kPpdfqdD6uyjzxjmvLq+FXceWPfqfuNXudpLaY/6lMd1vkIendZfzt98DnFSsH6aYK1b5/4hPpjZ87s6fT2vLuHaX03CNQcof306B26ood8T4jUvu08d1v5n8ucrxFP6EJ4D+ZBBuI0xEMjLDMJ6OdbSKEurZdwJ9+v1V49axrK04+q6sVx5V7mjr1/r79z51CF/1l1d13vc+wDn1++XD/sZrxCntdsf5GmAmY/85nt/mPvA/dg+EvZ+PRLiNZYw65AY1tzVdR3mevPSs4D4jItjIJpPvvcExgdDt1FTqgWZnrqsXC3jzsqtFqQfhN3T+xjrg9SpS/NFNQmpqVwt9c7KHdcuD3M/a3Z+dX2Q+q4bF89XSJ3CB63xwbDvyalK87CeMsz6I/+jvPeFua+6tE9xpZXugvSCcOfvOqz9EN3+vU69E1IH4TF/vkKOp/EB12MgcDut4/6cvjzm6nqnV66WeZjvoy7Le1xdh7n+6IU512t7DLP/2Gt1DWt/72vtTje/4hjIKnlqf/8ExkB204Q8FTBTP0TvW4dZB+PuXMcQP4S6vK8xJA8oDQLTF4gm7CHVIX5jqU/C2gfRYaZ9pH2M4eofAzF58r0nMD6HwHVKwNiV0+wchj+8AKanGBLb1vsaQ/IQqhf1dlauFsw1MMfWlfe4YPaZ0w9zXl12v7HUVzxfIZ7Kh3AMpKZTy31Bpg5r6quaWsYQf2nHZV4N7vv0w+xTv0dIDYTe0xq4r+vrdV2Huc/OD/FBuOsDnN/2Xj7s5+aTep/yoxgydQj7nw+i2wfmWD/Mun4Jyeu/R2skpNZYQvRdL5jzMMe9DyQPoX31Sdjnx1+yLD753hMYf5fVt+E01Y1hPV19EuLb1UHyEFonYa2bt69xEVIDMytXC6LXda1Vj9Ihvp43huTLe2/B7IPEvQ9EB873kMuH/dy8h7g/uE4NUB7/EQvw9flhJL4vnL78lgfUO4fh+8L8d/gQZbBGllarx6XdWzs/rP/M9rKuE1Knfs9/vod4Oh/C8R4CmSKETlO6X0i+xzsfxL/L26fn1SH1xvogunERonWvsYT4YGb1qNV9pa0WpL77ITqEu7z6kecr5HgaH3D99EAg0/ZJce/GkDyE5iVEh1C9E+a8/fVB8l2v/EorvS990jykt3HPq0vzneblLg/z/cr/9EDKfK7//gRuBuI0d7eGTFUfzLF15o13hNSb73WwzkN02NOeEI+xhFl/dG/rJKQeZprvhPh2OnB+Drl82M/NKwQyRQjdr0+P7LqxhNR3v3l1qf4qrT9y10PPLq8O671DdAjt94j21Wcs1Ys3A9F08j0nsP2kXtOq1bcFeTq6blw1tYzhvh/mPCSGsHrV2vWD+OBKvZ1w9QAjXf1rAdO3D5AYwvLUshCiw2usHscF1/rzFeLpfgjHJ/XjxOp6t7/K1TIP1+nC9bo89xbE2/sYW2vcaX5FvTDfQ31He+3yMPfrfuNO+6kbS/Xi+QrxVD6E4z0EMn14ju6/pnpc6hLmfuo/Rbj23/U87q+uuw+uPeD6v2XSVzWrZb4T0u+RDvHBlecrpJ/am+MxkNUTsNJ2+4VM2RpIvPPr63l1uF9vnf6imiytljGkZ2nHZV4NZp95iA4zzUv7GMuuGx85BmLRyfeewM1AYJ4+JN5tE+Y8zPGjuuPTUdewrq9cLftBfHDLnWenV99akF47n/qOkHqY2f2wz98MpBef8d89gR8bSD1htdx+XR+X+o6Qp+ZYU9cQHcLSnl27ez3S7b/zmX+V9rPO+MgfG8ix6Xn9+yfwYwOBPMFuBRJDqC59SmCdh+j6pPWQPNxSjzVSXe50SE/znZA8hPaTEB3CrhvbF+IDzn8ecvmwn5tXiFPr3O37VR9cnwZg13bowNc3sBCa6Pet2BzMXvXyHJc6zH495iXc98Gct+4V3gzkleLT+/MnMAYCmS7c57Nb6E8ZpG/X7acOa595/RLih+t3UDuvNRJSq1/2PMSnLmGt7/r0OritHwPRfPK9J3AO5L3nf3P3/wEAAP//3+mBggAAAAZJREFUAwDMCxDIWdGN4gAAAABJRU5ErkJggg==)

手机扫码阅读
