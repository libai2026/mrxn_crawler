---
title: "金和OA GroupUserSynchState.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html
asset_dir: assets/金和oa-groupusersynchstate.aspx-sql注入漏洞
---

# 金和OA GroupUserSynchState.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/15 11:33
- 636浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

文件大小转换

在线安全工具

网络安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GroupUserSynchState.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GroupUserSynchState.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **GroupUserSynchState** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitTxt();
  if (this.IsPostBack)
    return;
  if (this.Request.Params["UserID"] != null)
    this.strUserID = this.Request.Params["UserID"].ToString();
  string str;
  if (this.Request.Params["op"] == null || (str = this.Request.Params["op"]) == null)
    return;
  if (!string.op_Equality(str, "set"))
  {
    if (!string.op_Equality(str, "view"))
      return;
    this.InitGridView();
```

当 `op` 参数存在且等于 "**view**" 时，执行 `this.InitGridView();`

```
private void InitGridView()
{
  string str1 = "<root>{0}</root>";
  string str2 = "";
  int num = 0;
  string str3 = $"<record><SystemName ColumnName='{this.strSystemName}' Width='1.0'><![CDATA[{{0}}]]></SystemName><Flag ColumnName='成功标识'>{{1}}</Flag></record>";
  DataTable systemTableByUserId = new OpenGroup().GetUserPublishSystemTableByUserID(this.strUserID);
```

继续跟进`GetUserPublishSystemTableByUserID`方法

```
public DataTable GetUserPublishSystemTableByUserID(string UserID)
{
  string str = $"select a.*,b.System_ID, b.System_Name from outeruserrange  a inner join OuterSystem b on a.OuterSystemID = b.System_ID where a.UserID='{UserID}')";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

至此，就非常明了了，参数 `UserID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/GroupUserSynchState.aspx/?UserID=SQLI_POC&op=view HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GroupUserSynchState.aspx SQL注入漏洞](images/img-001-467d5fc72aba.webp)](https://image.mrxn.net/4b6b3c5a93d1422893f3dd48d8594d6f.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALbUlEQVR4AeyZgXrquA6E+c/7v/NeJuo4smwH2tMW9q75UEcajRRjxQXaP7fb7Z+v2j/l8bd9XF/aHmHNOb7Co/DBj6t651YtnBdaI/9vTAO51+/nu+xAG8h9wrdnrS4euAFdvTW1p/mMEPXmIGI40Tlj7TuL4awHXNphrctJ5zInH1i+XuVlrn0Gpbe1gZjY+NodGAYCMX0YcbVU3wWzPPR9smZVZz6j66DvB2dcNY7dx3FGOOuBnGo+cJyIRnzCgaiFEWdthoHMRJv7vR34sYH4rqyYXxrEXWPOWscQeTjfn5yzNmPNOX4Gcx/7j+rgXN8j7bP5HxvIswvYun4HvnUgcN4xEH5/uT569k7sqyKC6A9rdH9Ya6Lb7XiPAG75ARx87ZM13+1/60C+e3H/xX4/M5D/4k5+02seBuLjOcPVNSGOds67HsZc1l357iGEvo+4lbknRI115mdoDUQNMMismeEg/iBmWnMfkg6GgXTZHfz6DrSBAMcbGDzG1So9eSFEH/ky6OMZB6Fxf4gYxo+9M405o64hg+gj3/YZjbUQfWoMmGoIfGk/20Bap+28dAf++I75CtaVw3lXuF/V5HilgejjvBCCy/XylbMpvjKIHsAgcw+g3dlVZE3lc2zNV3GfkLybb+A/HAicdwzM/dndAL3WrxV6HnCq/fm+ERcO0O5k6P1a5vVl3hz0teaF1kOvMS+NzRzMtc5nhNBm7uFAsnj7P78DfyCmBIG+JETsO0DonHyZ42dQetkzWmsg1gCYujxF6p+tFX04V7kPyRRynXxgOJ21UDpZ5iHqzCkvcyz8N50Qrff/3vZA3mzEy4HoKMnyehXLII6efJk1EDxgqv2KAY5jLn01iJyLnHcsNAehdaxcNQjNigdaqvYBjnUCTQMcXCM+HNcKoddAH3+UdACjZjmQrnIHv7YDDwcCMUU4UXeEDE4OuFy09DLguNuAS72S0tuAo86x8jLHQug1ELF0MmlsEDkINJ9RNTJz0GuVs1ljNJ9xlYPoC9weDuS2H7+6A8OfTurVPdWMEBM1V2tyDKGFwJyz/0wfayH6QKB5Ye3jGEILJzqnukcGUWcd9LF4CA4CxX3F9gn5yq79YE37YlivAetJP3N3WWOs/WcxrK9pfe0HUQNYcrzXwBnXmiZMDnDUJap9QjRX+0DUwNf+PVD7qv8+Id6VN8E9kDcZhJfR3tThPH6wPoIqhF4rTqYjZ1M8M+eFMO8Dwc/qK6c+Noi6GrvGvBB6rTUzlF7mnHyZYyFEP/krg8eafUJWu/cifjkQiGnCiV6j7g7ZKhYPZx0gajD1uLKh4E4Ax5uv6+7UwydEDZz4sOgugNDf3eMJfXyQn/ixWjNEX2B/Mby92WP42LuaotYN5yTh+n3GfSrC2UM9ZwahyTn3ydzKh7F+pTV/1R+inzXQx+Yz1r7KQdTNcsrLlr+yXLTxd3egDUTTkT1zeelk1kI/efMZYdTAyOWama/ryuDrtap3b+j7QMRw/RtA9XBqFcsgOPmPDEZtG8ij4p3/nR1YDkR30cogJguB1n12ybUO1v0gchDoWogYGC5vjRPA8QkNMDWga4TAoZcvs1i+zPEMlZfNchB9Z7nlQGbizT29A18W7oF8eet+prD96cTtoT9OEDFgSfsrqI6kzAngOOIwojUZodc5B8E7vkJdv5r1EH1qPsfWGiFqAFPL15T7AIfOHETcmtwd5ypCaIH9xfD2Zo/2xRBiSp4eRJzXC8HBHF2bMdfLz7mVL50MzusozgZnDnrfOvd3nBGixhxE7Bqhc0Zx2SBqAEuOUwJjDCfXxB9O7rnfQz425V3gUwPJk8z+1YvJOvlAu4ug96/61Jx6raxqHcN5vVp7pXHOCNHHsbD2c6ycDaIOenRe+KmBqGDbz+7AlwYCMeG6NAgeqKnL2HcTcJyeS3FJQtQAJXM7esHI3+4P4Mjf3ePpNWQ8Evcf5u7uwyf0fR8WFMGXBlJ67PAbd2AP5Bs38ztaDV8M3VTHVOY4o3hZ5uSLs0EcXehRumfNvTLW2quctRBrcPyT6PXMruFcRYj1AfuL4e3NHsOvLDinBXTLBY43QuixE/1F4DvnmRbQrwHOeFXv/hlX2hkPcQ3XZw1EDnqcacxBaN1POAzE4o2v2YFhIJpStryszMvPOfkQE4fzv23SrUw12SDqrc+5lW+t0Br5M4PoDye6xghjDoKrGsfC2fVWnPQrGwayEm7+d3agDcTT9GWhvyvMC2GdU35msK6ByHkNEPGsjzXOQWjhPJVwcoClHdY+XfIjAI73zI+wgWszQq+FiOHE1uDCaQO50OzUL+5A+/O7rwkxUcf5LqicY2PWQt/HmozWZ06+eYgegOiHBhx3tOuvCiC00KNrha6Xn808nLWVs978s7hPyLM79Uu6Fwzkl17Zv/QybSAQx6++DggeaCng+NVgYnY8K+cYohZweUOg69sSE8f9Zmi5cxB9HQurRpwMQgtYcqwJaOiE9LbKQejNXyGEFth/Orm92aOdEE/a6HU6FlbO8Qwhpu4c9LF4CE69ZeKyibOZh6iBQPNC6DmYx4DknQHHCfD1hJ3gHoiT3d3lE6KPBdLbzBlnfBuIRRtfuwNtINBPdrYsCA0EesIQMZw4q6+c683X2LwQorf8bBA8kOnDr/0cCw/B/QfQnQyIGM4vmnfZ9Amn1gL1ljmGUVNz0tvaQCza+NodaP+g8oS8HMdwTticESLnmit0TcYrvXIQ/QGFU8v97FeheeA4DUCVTGPg0E+TD0hfM8ug72cNBA/sT1m3N3vsX1nvOhA4jw3QluljJTQJTI+yNNUgtDBi7Qe9xnlh7StOBlEDJ4qXQXDyq636Zd415qDvZz4j9Br3EFonXwajdp8Q7cwb2fDXXq8NYnowoidtnNWYq+gaoXPyZ+b83yLEa8h9IDgIzLmV7zVC1MCIroXIuUYIwUGgtcrZ9gnxrrwJDh97PSljXqc56CecNSvftav8jHeNsObFVbMG5uvLemsrQtTC+cUQgqvaWT9zVZvjK80+IXmn3sBvA4G4C6DH2RrrhB1ndJ05xxmhvxZEnDXVh9BAYM0r9jUrKlfNGoh+joUQnGsgYuVkEDGMp0l5mWuFimXys8HZpw0kC7b/uh1on7I0uWxXS4KYqDUQMYxozVcQHveDU+NrwMnB6Tv/Wcz7In9WD3Ed5yBiGNGaGe4TMtuVF3J7IJeb//vJ9rG3XlpHs5o15h3P0BqII3ulsdZorWOhOaO4lVWNY4i1wPgmbE1G94eoy7nqW1ux6hRD3y/X7BOiHXoja2/qEFOD57G+jjzpmoOxb9U4htA6Frq3/GwQWiDThw90fwR1D+EhmPyAqIETpZdBcJOyRsFaox4za8V3Z5+Q+ya807MNZDa5Fbd6ARB3B5xYtbmnc3DqAdPH3Q0c2MjizPoVSQshegGNc30jnnCA5Zr+ph+w/2N4e7NHOyFeF8T0YURrnkHfKUbXwNi3aqw1L4Socw4ihhGtUZ2sxuIg6mY55WXOGcVlMy+E6Ac9KmeDyDk25p7DQCza+Jod2AN5zb4vr/otA/GRy1eBOJ4QaE3GrJefc/LFVRMvMy/fZs4I/bUhYji/GFp7hRB11kDEvq7QOaM4meOMEPWZs/8tA3GzjX+/A986EN0Rts8sDeKOgTU+069eu8a5B/TXcg5O3lzFq75VO4uv6r91ILOLb+5zOzAMxNOb4Wda13o47zwIv2pqnK/nHEStcxAxYKohcHyBg0D3yGgxhMax0Dr5MggNjGitEULjWKgej2wYyKOCnf/ZHWgDgZgoPMbVkuCstQaCc6w7xQaRgzlaJ4TQyF8ZhMbXqgiRB1qq9mqJuwMcJ+zuHs+qzfEhmPyA6AHrT3ZwatpAJr029YId2AN5waZfXfJ/AAAA//8iPjdsAAAABklEQVQDAHSIJKp68r3NAAAAAElFTkSuQmCC)

手机扫码阅读
