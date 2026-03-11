---
title: "sublime text3安装phpfmt插件格式化php"
source: https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html
asset_dir: assets/sublime-text3安装phpfmt插件格式化php
---

# sublime text3安装phpfmt插件格式化php

[Mrxn](https://mrxn.net/author/1)- 发表于2015/12/9 12:18
- 22642浏览
- [0评论](#comment)
- 40分钟阅读

深入探索

软件包管理系统

sublime

软件

---

sublime text3也支持php格式化的插件了，在这里向作者致敬，感谢他开发出这个插件，如果你不知道sublime就不要往下看了，免得浪费你的时间，[[![sublime text3安装phpfmt插件格式化php](images/img-001-30ce4780af7f.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201512/thum-faab1449638381.jpg)](https://mrxn.net/content/uploadfile/201512/faab1449638381.jpg)

首先是你的sublime安装了package control（插件管理包），如果没有安装，请自行百度搜索安装，一大堆教程，在你安装了package control之后，引用原作者的话就是：

开发工具

#### Install this plugin through Package Manager.

- In Sublime Text press `ctrl+shift+P`
- Choose `Package Control: Install Package`
- Choose `phpfmt`

1. 打开sublime，在sublime界面 按 Ctrl+shift+P 组合键，
2. 输入 install package,找到Install Package，并回车打开，
3. 输入 phpfmt 找到并回车安装，等待安装结束，

做完上面的工作，还不能使用phpfmt插件的，还需要配置插件所需要的php环境，最新版的phpfmt插件需要php5.6或者更高版本，这里，博主离线了两个在百度网盘，分别是php5.6和php7.0的非安全线程压缩包（都是64位的），直接解压到你想放的目录即可，如果需要其他版本或者是32位的请自行前往php官网下载，百度网盘地址：<http://pan.baidu.com/s/1kUn5zxl>  官方下载页面：<http://www.php.net/downloads.php>

深入探索

JSON处理工具

编程语言教程

SQL注入检测工具

将自己需要的安装包下载下载后，解压到你想放的地方，比如博主，防止wampserver的php目录里面，这是方便我的wampserver使用，你们可以根据自己的需要放置；接下来就是打开phpfmt配置：

软件

Preferences > Package Settings > phpfmt > Settings - User

我将我的配置贴出来，供大家参考：

```
{
    "enable_auto_align":true,//自动调整对齐
    "indent_with_space": true,//自动空格
    "psr1": true,
    "psr2": true,
    "version": 4,
    "php_bin":"D:/wamp/bin/php/php5.6.16/php.exe",//php路径
    "format_on_save":true,//保存的时候自动格式化
    "option": "value"
}
```

深入探索

SQL

恶意软件分析工具

Web安全书籍

其中的php\_bin 很重要，就是你存放php的路径，其中的有些配置我在百度没有搜搜到，在国外的网站上看到的，试了一下还不错，原地址：<http://stackoverflow.com/questions/29350807/sublime-text-3-php-fmt-wont-work> 有兴趣的童鞋可以去看看。

搜索引擎

配置完之后，重启sublime text3，打开你需要格式化的php文件，快捷键：Ctrl+F11 或则是在按下组合键Ctrl+shift+P后输入phpfmt 即可选择想要执行的操作，下面是一些常用命令：

```
The following features are available through command palette (ctrl+shift+P or cmd+shift+P) :

phpfmt: format now //立即格式化 ctrl+F11
phpfmt: indentation with spaces
phpfmt: toggle additional transformations
phpfmt: toggle excluded transformations
phpfmt: toggle skip execution when .php.tools.ini is missing
phpfmt: toggle auto align
phpfmt: toggle autocomplete
phpfmt: toggle dependency autoimport
phpfmt: toggle format on save
phpfmt: toggle PSR1 - Class and Methods names
phpfmt: toggle PSR1
phpfmt: toggle PSR2
phpfmt: toggle smart linebreak after open curly
phpfmt: toggle visibility order
phpfmt: toggle yoda mode
phpfmt: analyse this //Ctrl+F10
phpfmt: build autocomplete database
phpfmt: getter and setter (camelCase)
phpfmt: getter and setter (Go)
phpfmt: getter and setter (snake_case)
phpfmt: generate PHPDoc block
phpfmt: look for .php.tools.ini
phpfmt: reorganize content of class
phpfmt: refactor
phpfmt: toggle PHP 5.5 compatibility mode
phpfmt: enable/disable additional transformations
phpfmt: troubleshoot information
```

phpfmt插件作者项目在github的主页：<https://github.com/phpfmt/sublime-phpfmt>

实际效果看下面是我的亲测的code：

```
<?php
for($i = 0; $i < 10; $i++)
{
if($i%2==0)
echo "Flipflop";
}

// 格式化之后的样子
<?php
for ($i = 0; $i < 10; $i++) {
    if ($i % 2 == 0) {
        echo "Flipflop";
    }

}
?>

<?php
$a = 10;
$otherVar = 20;
$third = 30;

// 格式化之后的样子
<?php
$a        = 10;
$otherVar = 20;
$third    = 30;

<?php
namespace NS\Something;
use \OtherNS\C;
use \OtherNS\B;
use \OtherNS\A;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// 格式化之后的样子
<?php
namespace NS\Something;

use \OtherNS\A;
use \OtherNS\C;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// PSR version

<?php
for($i = 0; $i < 10; $i++)
{
if($i%2==0)
echo "Flipflop";
}

// 格式化之后的样子
<?php
for ($i = 0; $i < 10; $i++) {
    if ($i % 2 == 0) {
        echo "Flipflop";
    }

}

<?php
class A {
function a(){
return 10;
}
}

// 格式化之后的样子
<?php
class A
{
    public function a()
    {
        return 10;
    }
}

<?php
namespace NS\Something;
use \OtherNS\C;
use \OtherNS\B;
use \OtherNS\A;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// 格式化之后的样子

<?php
namespace NS\Something;

use \OtherNS\A;
use \OtherNS\C;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();
```

如果需要下载使用新版sublime text3 并且免费注册，请查看这篇文章：

## [(Mrxn分享)Sublime Text 3 Build 3065 安装版注册+汉化](https://mrxn.net/tools/3.html)

- 标签：
- [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#php](https://mrxn.net/tag/php)
- [#mrxn](https://mrxn.net/tag/mrxn)

---

文章目录

- [1.
  Install this plugin through Package Manager.](#toc-1-)
- [1.
  (Mrxn分享)Sublime Text 3 Build 3065 安装版注册+汉化](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
