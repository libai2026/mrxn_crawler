---
title: "孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxFormDefault-sqli.html
asset_dir: assets/孚盟云crm-ajaxformdefault.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/18 08:31
- 237浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

Docker加速服务

传输层安全性协议

授权

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxFormDefault.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxFormDefault.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxFormDefault** 方法的实现如下

[![孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞](images/img-001-172b898f5aa8.webp)](https://image.mrxn.net/86e21924ed164f34a3f350508e880d5c.webp)

当**action=getEditProductPic2**时，看下`getEditProductPic2`方法的实现

代码安全审计

深入探索

SQL

SQL注入防护

恶意软件分析工具

```
public string getEditProductPic2(HttpContext context)
{
  string str1 = context.Request["FID"].ToString();
  string str2 = $"{HttpContext.Current.Request.Url.Scheme}://{HttpContext.Current.Request.Url.Host}:{(object) HttpContext.Current.Request.Url.Port}";
  DataTable dataSource = new CreatePageDao().GetDataSource($"select * from bpProducts where FID='{str1}'");
```

参数**FID**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成SQL注入漏洞。

当**action=GetChilDept**时，一样的存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞](images/img-002-ebb7e0bfaf4e.webp)](https://image.mrxn.net/22134d911d834caa8c49fe79b4bb613c.webp)

action=SearchChilDept

漏洞扫描服务

[![孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞](images/img-003-dad2c981f210.webp)](https://image.mrxn.net/e312417b95d04777bd2ce37e8162902b.webp)

action=sendProductMessage

[![孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞](images/img-004-d111b398f2fe.webp)](https://image.mrxn.net/e139231202ea4d548c3cea9bc7cb9411.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxFormDefault.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=getEditProductPic2&FID='SQLI_POC--
```

[![孚盟云CRM AjaxFormDefault.ashx SQL注入漏洞](images/img-005-bda2b243f392.webp)](https://image.mrxn.net/fc9986d7139a4e9daa5d7a79f329e9cd.webp)

成功通过报错注入在响应回显数据库版本信息

物流软件安全

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALZ0lEQVR4Aeyd0XbbSA5Edef//zkTuHIpNsgWJSfH0kP7bM8lCgWw3aBiS5Pd/e92u/36zvr158vaP+EG9c7NMLnQb9pYqkv1YteMZXn2S33GvXd/3f3m1I2/wxrI77r1n085gW0gv6d7e2bNNg7cgEPanofEHwH4qoNw5u86jP7Kw6j9ucXWvzy1ut5jSB/1Tkgewp43rns9s/QXt4FUsNb7T+AwEMjUYeTVVn0S9F3FkP4zPyRvH0isX0J0YHuFm5O9h7GE9DCWvV5dmr8ipD+MPKs7DOTMtLSfO4G/HohPC2T6bh3GuOvWdR1S1/PdZ35PPZ2Qnt/VIfUQ9j7uoevfif96IN+56aqZn8A/G8jsKYHzp8ot9boew3k9RIdr2lNCaozdC4y6ealPznTz3+E/G8h3br5qjidwGIhT7zyWRoE8VbDj7+tkf38M8OvX128/kLx9IfHM13VjaZ8zdg/kXhBaA2NsHUTvca8zf0XrOs/qDgM5My3t505gGwjkqYDHnG3N6Zs3hvS7iq3rhLF+lgd66hBf7cH8ofBCAL4+Deg2iA6Pua/bBrIX1/X7TuA/n4pX2bcMeQq6bl84z1/5re8+Y/NFNQm5Z+Vqqdd1rVms/iyrVy39df3dtV4hnuKH8DAQyFMFI90vRDeW/YlQh3M/nOvW2Q/OfRAdjuw9jCFe4xn7vY319xjSF85pnYRzH3A7DOS2vt56AttAIFPr03d3cJ7XD8lDaF2nfvUeQ+oh1AdjbN2eeiWkBkK9kFjfjPrNw3ld9+nvhNR3v3FxG0gvXvF7TmAbSE2nFmSKs+1A8jBSf/WoBcnX9X7BqEPiXm/NTv96x68OY135zM0IqTEPiau2FjyOrSvvfkHqzHfqVTeWkHpg/Qy5fdjXf3CfDsz/rZv7dsozdp8x5D7GM8Lo8z5XfkgdHNlrIR51OI+v7m29PkgfCM3DGKufcfsj6yy5tJ8/gelAnHonnE8bXtP9Vu1v3AnpC6F56/Y09yyt7X51yD1hpH4Ydet6/lm96qYDqeRaP38C20CcIoxT71vSN9Mh9ea7v8cw+q2T+qX6I155Z/muG8vZPWf5rkO+164bF7eBzG629J89gcNAakq1ZtuATNk8JIawamv1vHFneWt13RjS1/hvWPepBWPP0mrZG5KHUL08tWDUYYzLUwvOdftB8nDnYSCaF99zApcDgUzP7dXka81iOPdXTS0Y8/aBUYfXYvsUIbV1v1ql7Vdptb603T9grCtPrZ3l67K0Wl/B7h+QeqXy1ILoEPZ8eVyXA7F48WdOYPs3hjBOz9s7OUgeRnafcSekbtZPvdepS0if7tvHevfa2TWMvXodJA8jey/rpHlInbo0LyE+YH2Wdfuwr+2PLKcHmZax+zWW6leEsR+Msf3gXLc/nOchOqD1QOD0b4V4bwtg9Jnv1K8OqYPQvIToMNK8fYrbQEwuvvcEpp/2wvk0IbrbhjGuKdeC6HVdCxLP6roOo9+8hOSrt6vnjCWkBsKu9z49D+d1+qyH0Wdedh/ED6yfIbcP+9p+y5rty2ma77G6hExbH4yxvlfz1kH6Ge9pz722vzYv97m6hvSGsLRa3Q/Jd728j1b3G++5foY8OsE35LafIU4JxulDYvcGY3ylv9pXv31fIWRvsx6Q/FVP6yF+CK/qdvnh0n6KkH4QqhfXK6RO4YPWNhA4Tmu/T0i+T9u4E+KH0Py+Z12ry9JqQerqer/0SYgP7n8fAKLt6+q615RWS12WVst4xvLUMg/jfdXLs1/qcp/bBrIX1/X7TmAbyNm0zrYF41MAj2N7QHwQdr3H7kf2PIx9Kg+jBmNcnlr2hDEPiWFk1ewXJK8GY9x1eC4PrPchtw/72t6HwPkU3a9PVad5SL15deMZ9Ul9xvB6X2vtJSG9en4Wqz9L79P5bH35tj+yKljr/SdweB/idGdbg/Ep0zerg/gh1A+Jex1Eh9A8JLZeQnRAaSPw9SkvhCYgMYw07z2NIT5jCa/pV3WVX6+QOoUPWmsgHzSM2so2EMjLD8JKnq3+cu4eSP2Vb5ZXl/bvcdcrryZLe2bp7+y15tWNO6/y+s9820A0Lb73BKYDgTzpbg8Sw0jznRCfen8aIHkI9UmIDiOv8oCWjcDXD/dN+HMBow6J4Zx/yr56wf2jmq7DWG9eehYQn3FxOhCLF3/2BA4DqSntl9vZa3Xddci0u17eWuqytP2CsX7m29fUtb5HLF8tyD0gLO1s9V56YKzrPmP9PYbUd924eBhIiWu97wS2j05mW3DakOlC2P36ug7xQzjLq0N89oPEEOqT+s4IY0332KNTnzqkz0zX1/PqnZB+EO7z6xWyP40PuN4GcjVd87LvHTLtWV4d4rNeXarLmW5+T0hvCK2FxBDua165hvN679N7zXR9Z/ltIJoW33sC20DgfPoQHUY6XYhu7LcD0Xv861f+J//UJZz7YdT1S0ge5u8L9Eq418DxWp/0e5OQGvMSosNI87L3gbt/G4jmxfeewPbxu9uATMvYaXaalzDWqXfC6IPEs/7qV30qD+e9eo9Z3PXqWQvSF0J9EqKXt5a6LO1smd9zvULOTuqN2mEgTgsydXhM926dsVSX6lIdch91CdFnPvU9ITUwctaz68b27DGMffVJ/TD6ZjrcfYeBWLT4nhOYvlN32tLt9Vgd7lMGlLdPRoGv6y3x4gWM9e4DogNbR3MKxp3AsCfz1sGYh8T6JESHkfbR9wzXK8RT+xBuA3F68HjKkLz7t85YznTzV/xOPWRvEPYeEN17z/IQX88bQ/L2mVH/LA/pA3duA5kVLf1nT+DwPqTfHjI9dacu1WXXZzGkL4TWd/Z685A682eEeKyZEeLrPfSrQ3zqnfokxA/hlb/q1iukn9Kb4+23LMgUa0pny31CfMbSGmOID8Ke16cu1SWk3lifhOQBLV+/OcHxsy0NwOaBuw+i65MQ3XtKiK6vU5+E+CHs/orXK6RO4YPWYSCQ6UHY9+q0uw7xQ/hqXj+M9d5Pwjxvjyvaq/u6DuO9YIz1y94Pzv36YMyXfhhIiWu97wQOA3Ha0q1BpgkjzXf/LO46pJ99OiF5CM1DYrjT3N/eA9LTPp2QPDym+5EQv7GE6MD6L+zcPuzr8AqB+7SAbbv9KTEBDL+xdN26mW4e0kffs7S+eFVTnlr66rrWLIZxTzDGVfto2RdSp1ddqhcPA9G0+J4TmL5Tr2nV6tuCcdrl2a/un8WQPhDao/tnuj5IPRypZ0ZIjfeAxHd/riC6vqi34U8GiAfuvLUvSM4+EqID62fI7cO+tnfqTkvO9tnzkOnqn+Vh9HU/JD+r1y/1nVEPpOcsVpf2MpbqMPZT7z512fPGUl9x/QzxVD6E288QyPThObr/mmotY0i9ceVqzWIY/ZAYQutmhPiAmWX4P4KpvQBff/73Aohenlo9X9p+9bwxpI+xhFGHxHDneoV4Wh/CbSD7yT+6nu0bMuVeC9FndV3v9T3f471/lpvp1kL2OIuth/hgpHlpH2PZdeM9t4FYtPjeEzgMBMbpQ+LZNmHMQ2IInX6vV++E1EHY8/aB5OFIPRJGT9e9B8TX8zDq5jshPhh55dvnDwPZJ9f1z5/APxuIT1n/FiBPS9eNIXkI7SO7T/0ZWqvX+IpXfvOd9u26sXljCfnegfVO/fZhX//sFQKZ8rPfHzz2Q/IQ+jTZH6LDkXokxGMPGGN9Esa8dRKSh9A6CdEh7PosLv2fDaSarfX3J3AYiE9B5+xWr/pgfGpmfdXtD2Od+p7WwLnXvDXG8Nj/qk//Ffs+yn8YSIlrve8EtoFAnhJ4zGe32qcP6dt1+6nD6IMx1i8hebj//Sp76ZkRUqtf6ofkIVSXcK7P+vQ6ONZvA9G8+N4TWAN57/kf7v4/AAAA///2eF04AAAABklEQVQDAEVOecgL7uuWAAAAAElFTkSuQmCC)

手机扫码阅读
