---
title: "金和OA AcceptGetFileNameEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptGetFileNameEdit-sqli-2.html
asset_dir: assets/金和oa-acceptgetfilenameedit.aspx-sql注入漏洞
---

# 金和OA AcceptGetFileNameEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/6 08:05
- 514浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

漏洞扫描服务

编码转换工具

Web安全书籍

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptGetFileNameEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"
>
> 代码安全审计

# 漏洞分析

根据 AcceptGetFileNameEdit.aspx 的源码，在 bin 目录下查找 JHBase.Web.AcceptAip.dll 将其进行反编译后找到 `AcceptGetFileNameEdit` 的处理逻辑

漏洞修复方案

```
public class AcceptGetFileNameEdit : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    string SlaveID = this.Request["fileId"].ToString();
    string empty1 = string.Empty;
    string empty2 = string.Empty;
    string empty3 = string.Empty;
    UploadFile.GetFileInfo(SlaveID, ref empty1, ref empty2, ref empty3);
    string str = this.Request.UrlReferrer.AbsoluteUri.Replace(this.Request.UrlReferrer.LocalPath, "");
    this.Response.Write($"{str.Substring(0, str.IndexOf("?")) + this.Request.ApplicationPath + empty1.Remove(0, 2)}|***|{empty2.Substring(empty2.LastIndexOf(".") + 1)}|***|{this.Session["SESSION_AIP"].ToString()}");
    this.Response.End();
  }
```

深入探索

网络安全课程

传输层安全性协议

Docker加速服务

参数 `fileId` 传入 `UploadFile.GetFileInfo` 方法中

跟进 `GetFileInfo` 方法

```
public static void GetFileInfo(
  string SlaveID,
  ref string FilePath,
  ref string FileName,
  ref string FileType)
{
  string QueryString = $"select FilePath,[FileName],FileType from  Files where FileID in ({SlaveID})";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  if (((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
    return;
```

参数 `SlaveID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AcceptAip/AcceptGetFileNameEdit.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileId=SQLI_POC
```

[![金和OA AcceptGetFileNameEdit.aspx SQL注入漏洞](images/img-001-68096a3f0ced.webp)](https://image.mrxn.net/c1b07205e4344732b3ee0ffb8f42f80f.webp)

成功延时 5 秒

编程

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALUUlEQVR4Aeyd63rjNgxEffr+77wNMnsUEiJtZ2/2D+UrOprBAGQIaZXL9ut/t9vtx6/Ejyc/em/Lut5593Xe/SPX21FP1zvXt8OdX31X94xeA/nwXf+8ywkcA/mY7u2Z2G0cuAGntD1NAEuf+e6XQ+rk+kc0B/Gag+c4zD77ib0fzH7zonWPUH/hMZAiV7z+BE4DgUwdZtxtFeLb5Xd6v2u6D+a++rtPvRDmGr2Vq5CLEH/lxuh5uahX/ggh68CMq7rTQFamS/t3J/DHBuJdA+u7wLzopwjxd928CPHJRYgOnN6Bejq6ltjznUPW6Lr82T767+EfG8i9Ra7c8yfw2wPZ3R1dh9xlMKNbhbVu3n4Qn/qIkByscfTWNcy+0ipcq64rOi+tYqdX7lfjtwfyqwtfdesTOA3EqXdcl5/Vz7of9c1/cpC7MOzjxwIfufLIO1ZuDPOw7jN6vbZG7DqkV9f1Q/LPcn07dJ2OK/9pICvTpf27EzgGArkr4D72rUH86jBzde8OSF6+y6vD2t/zgNKBrgF8/nRAfhgeXHR/55ZD+stFiA73UX/hMZAiV7z+BP5z6t9Ft26dXITcFebhOb6rV+9o/8Keg/tr6q/ais4h9eo7rNoK83X9q3E9IZ7im+B2IJC7A4LuF8IhqL5DiM87pvtgzncfJA9B6yEczqjHXhCP3DxEl3fc+bve63Ycsh4EV77tQFbmS/v7J/AfZFoQdMl+F0DyO73X6RMh9fpE83J4zqff+sKu7TjMa0A4rNE+Iqx9cF+3vvZaIYevuusJ8VTeBI+vsh7tpyZaAZlmXY8B0SFoP1hza2HOq4v2ud1u06V5SD18/bR3Mn4Q+PLAl88eHT9Klv90n7ybuy4Xu3/k1xMynsYbXJ8GArmb3Fufaudw328fsdd3Dvf7db+8EOZa1+wIz/l2dZB6CHafvPZUAbMPZq6/8DSQEq943QkcX2W5hZpoBcxThHCYsbwV1sM6X54KfR0hderwPW7dCmvdMfTAvIa6ONbUtXrHylWow3N99Y94PSHjabzB9fFVVk24AubpQnjlxuh7N9d1SD3MqA+iy+0jdl3+KwjzWrsefe0/5YOsD0H7ul7h9YR4Km+Cp3dI31dNrUIdMt3SKnZ65cbQJ0L6yPXKRYgPguo7f+Vh9pZWca+m8gakHoLqon3g9/L2g/QBbtcTcnuvj+MdApmS0+/bhDkP4RC0DsIh2PvI9YsQP8xoXrT+GYT02nk/e378jh/ig6D6rk69++TwvT72K7yekDqFN4rjHdKn6x4h0+5cv2i+I8z1Pd/5d/tB+gNHK3uIwOfv1A/DzwuIru+n/OmFr595wdqnf4eQOgjufKN+PSHjabzB9fEOcS/9bul6z8M8/Z63/hH2us5hXmfVr9fo2enmO+78kD1A0DoIh6B6x94X4lcvvJ6Qfmov5sc7xH3APDV1EZKHoLoI0Wva9wLis06EWYfw3kv/iBAv3Ed7WQvx73j36+vYfXIRsg4EV/r1hPRTfTE/BgKZWt9Pn6Jc7P4dh/SHYK+HWYc1h+iuY58V6hH1PMvh/lq7Puo73O2j9GMgu+JL/7cncPoqqy8PuUtqehUQvvPt9KodA9Z9/nR99XPdul6FeVjvCWYdwiG46LmUXMcknOuvJ8TTeRM8vsrq0+v7g0xz51MXd/WQPuZh5uodIT4IrtaB5CDYe3QOz/l6XeeQPhB8lIf4Vp/D9YT003sxP94hkKk92g/EB8GdH5L3Ltjhrv6RDukPX/ioxjykxj1BuHnRvFxUF9U7wtxXv6gf4gOu34fc3uzjeIe4rz69rpsXzYuQae+4utj7QOq7vuPqI9pbhPSEoF6YuXqv2+n6RH0dzUPWgxlH//UO8bTeBE8DgUxvtz9Y5yH6OO3xGpLvfWGt67MHrH0QHbDkQGsVOlcHPn8HItcnQvIQVNffEeLrunUdR99pIGPyuv73J3AN5N+f+d0VTwPxcaqqVezy6rB+XO0F9/PdB/f9rltorQiprVzFs7o+sWor5JC+EFQXy1shFyF+2ONpIBZf+JoTOA0E5um5LZh1CDe/Q4iv7pgx9KvJO5oXzUP6whn19Bp1EVL7yKf/EUL6wYzW9XU6L99pICVe8boTOH500qfVuVtUF9VFdchdIjcP0Tvvvp6HuW7l7xrMNRCuT4Toj9Y039E+6p2rw3od84XXE1Kn8EZx+tGJe4NMs08bokOw563vOqz93berf+SrPGSN3gOil6fCPKx18+WtgPs+SN46sWor5GJpFfIRrydkPI03uD7eIX0vNcGKnV65CsjdATNaB9HLWwHhPS8vT4VchNRVrqLr8PVXP83tEOZeEL7zq0N8tf4q9IkQv3yHY6/rCdmd0ov0YyCQaTot9wPRd1zdOhFS1/ntZkWw5yF1EIxr/2/rC3XVdQXMPSC8chXd/yyH9IFgr4O1rq8jxA9cv6C6vdnH8YS4L8i05HUnrQLiMwfhvU4u6pfDXKeuryPED0H9hTBr1lZuFRA/BHd+SN4e3QfJQ9C8aN0zeBrIM0WX5++dwDGQ3TQhU4cZf9UPz/XxU4a1f7e+dfcQ0nPXA5KHoD6x91YXIXUw46O6qj8G0s0Xf80JPPxOvW+rplihDrkLSqtQF0urgPjURYhenjHMi+YgfjijHmsgHvWO+tQh/q7LIXkIWtfzXTevDqlXH/F6QsbTeIPr7Xfq7s2pymGebs93DvGri/bbIaSu53u9vLB75TD3gnAI6nsWa60KSD0ES6uAmZdWAdH7OhAduL4Pub3Zx/EOgUyp7w+i14THgOg7/06Huc6e+iH5nQ7Jdz9EB0yd/gcvwPTXfQ5ju9itrQ3mPvoheucw67s+pV/vkDqFN4rjHeJU3ZtcVId52hBuXn/HXR7men0w673fPQ6phaA9dwhrH6x11+791GGu67p8hdcT0k/1xfx4h/R9wDxl8051x9W/i7Ber/eBvQ+S63uEtd59rgXxy8Wd3zzMdfohunznL/16QuoU3iiOdwjMU9xNE+Lzc4BwuI87v+t01C9C+u+4+ojP9tQ31tZ112HeQ3meiUd9IH2B6/uQ25t9nP7Igq9pAcd2nbIITF/Tqx8FDy66H9IPgpbr26G+Qj11XQHpBcHSxuj+zvWqizD3g3Dz1omQvFzUP+JpIJovfM0JbL/Kcmp9W5Bpmxdh1nudXL/8EUL6wvexrwXpoQ7hEHQvX/noMKO+jhCfOsxc3f5yiA+43iG3N/s4vspyauJunz0Pma46zFzdfpC8/FnsfeQrtCes14LovfZR3c5vXc/LzUPWhRn1FV7vEE/rTfB4h8A8NbjP+/4h/ppyBYRDsLQxILp9zMk7wuw3D9EBpRM+6n0q+Cns6oDPrzAf5X+22YL1kH7A9Q65vdnH8UeW03qEff/dD5l2162D5DuHWTf/CMd1dl6Ye1sDsw4zt5/+HVcXu19d7Hl54TEQzRe+9gROA4HcJTDjbpsQ3y6vDrOv7oYK8zsszxj6IP3gjHrEsb6uuy4Xy1MBc2/z8JwO8VlXPSvkMOdLPw2kxCtedwJ/bSBwnv74acKcrztnjNFb1xC/ntJ6mBN7Xg7pBTNaB9H1P9L1dbROhPSFYPcX/2sDqeZXfP8EfnsgTt+lO1fvqE80D+u7p/vkI+56wNxzrBmvYe2D6KO3rl1vh5A6COqr2go5JA9c34fc3uzj9ITU5Fbx7L4h09757Q1rn3nrYfZBOAT1FUI0e3QsTwXEV9cVMHPrIHrnEL1qK8yLpY2hLsJcP3pPAxmT1/W/P4FjIJCpwX3cbRFS513QfeoQn3mYubponVxUh9TD8/8Vrj062lNdDllDLuoTYfZ1Heb8qs8xEIsvfO0JXAN57fmfVv8fAAD//wz/D5AAAAAGSURBVAMANEHsmy1lFUMAAAAASUVORK5CYII=)

手机扫码阅读
