---
title: "Burp Suite新手指南"
source: https://mrxn.net/jswz/burp-suite-for-beginners.html
asset_dir: assets/burp-suite新手指南
---

# Burp Suite新手指南

[Mrxn](https://mrxn.net/author/1)- 发表于2016/3/30 12:25
- 5842浏览
- [0评论](#comment)
- 37分钟阅读

深入探索

Web安全课程

VPN服务

文本剥离工具

---

**Burp Suite想必大家都用过，但是大家未必知道它的所有功能。因此，本文的主要目的就是尽量深入介绍各种功能。BurpSuite有以下这些功能：**

[blue]

截获代理– 让你审查修改浏览器和目标应用间的流量。爬虫 – 抓取内容和功能

Web应用扫描器\* –自动化检测多种类型的漏洞

Intruder – 提供强大的定制化攻击发掘漏洞

Repeater – 篡改并且重发请求

Sequencer –测试token的随机性

深入探索

Web安全书籍

Docker加速服务

网络安全培训

能够保存工作进度，以后再恢复

插件\*–  你可以自己写插件或者使用写好的插件，插件可以执行复杂的，高度定制化的任务

\*表示需要Burp Suite Pro授权。

[/blue]

代理与过滤

## Intercepting Proxy（截取代理）

Intercepting proxy是针对web应用渗透测试工具的功能。Burp Suite的代理工具非常容易使用，并且能和其他工具紧密配合。要使用这个功能，第一步就是建立代理监听(Proxy–> Options功能下)。我的设置为了默认值localhost (127.0.0.1)，端口为8080。

[[![Burp Suite新手指南](images/img-001-32bd8048519b.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-42281459312163.png)](https://mrxn.net/content/uploadfile/201603/42281459312163.png)

深入探索

网络安全会议

物流软件安全

Windows安全工具

你可以点击编辑(“Edit”)进行修改，或者添加新的监听端口。一旦建立好，你就要到浏览器的网络连接设置处手动配置代理设置：

[[![Burp Suite新手指南](images/img-002-81719be488ad.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-79741459312388.png)](https://mrxn.net/content/uploadfile/201603/79741459312388.png)

我们现在可以访问我们要测试的应用，然后看到发送的所有请求了。到Proxy –> Intercept标签页，然后确保截获功能开启(“Intercept is on”)，然后就能看到所有的请求了。

[[![Burp Suite新手指南](images/img-003-191c1a7103e8.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-00a01459312448.png)](https://mrxn.net/content/uploadfile/201603/00a01459312448.png)

你可以修改请求，然后点击“Forward”发送修改后的请求，如果不想发送某些请求你也可以点击“Drop”按钮。“Actions”按钮下还有很多其他的功能。

[[![Burp Suite新手指南](images/img-004-4d570607bc18.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-2ac31459312531.png)](https://mrxn.net/content/uploadfile/201603/2ac31459312531.png)

如果你想回过头看下前面发送的请求，你可以切换到Proxy –> HTTP History标签页，这里有所有的请求列表，还有些详情如响应的长度，MIME类型和状态码。如果你修改过请求，你会看到两个标签，分别是修改前和修改后的请求：[[![Burp Suite新手指南](images/img-005-89122f0b4956.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-3d551459312593.png)](https://mrxn.net/content/uploadfile/201603/3d551459312593.png)

另一个有用的功能是自动修改请求/响应，功能位于Proxy –> Options。通过这个功能可以去除JavaScript的表单验证。你也可以用正则表达式匹配替换请求/响应：

[[![Burp Suite新手指南](images/img-006-3d15b620c5ca.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-46da1459312803.png)](https://mrxn.net/content/uploadfile/201603/46da1459312803.png)

## Spider（爬虫）

当你在对web应用进行初步检查的时候，Burp Suite的spider工具非常有用。当你浏览Web应用时，它会从HTML响应内容中主动生成一份URL列表，然后尝试连接URL。要使用爬虫功能，我们首先要切换到Target–> Site Map标签，然后右键域名，选择“Add To Scope”：

漏洞修复方案

[[![Burp Suite新手指南](images/img-007-4c76cbb71cd8.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-bf641459312912.png)](https://mrxn.net/content/uploadfile/201603/bf641459312912.png)

所有加入的域名都在Target –> Scope标签页里。你可以手动添加域名，修改，或者添加需要配出的URL（比如如果你不希望对“联系我们”的表单进行自动化测试，就可以把它排除掉）：

[[![Burp Suite新手指南](images/img-008-3352a5e33a96.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-a9c51459312989.png)](https://mrxn.net/content/uploadfile/201603/a9c51459312989.png)

如果我们现在进入Spider –> Control标签，就能看到有些URL正在排队中，注意看下面，爬虫只会对scope中的域名进行测试：

[[![Burp Suite新手指南](images/img-009-d52363ca7d0c.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-c5c41459313022.png)](https://mrxn.net/content/uploadfile/201603/c5c41459313022.png)

回到Site Map我们可以看到URL的列表，黑色代表我们已经成功访问过那个页面，爬虫确认过是有效的。灰色代表爬虫在HTML响应中找到了这个URL但是还没有确认是否有效：

[[![Burp Suite新手指南](images/img-010-96354f48b977.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-f6501459313184.png)](https://mrxn.net/content/uploadfile/201603/f6501459313184.png)

基本的设置后，我们返回到Spider –> Control标签，点击“Spider Is Paused”按钮运行工具，它会尝试连接所有之前找到的URL，包括在运行过程中找到的新的。如果过程中有表单需要填写，它会弹出表单供你填写，确保能收到有效的响应：[[![Burp Suite新手指南](images/img-011-6a2c5c20c292.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-9b4f1459313227.png)](https://mrxn.net/content/uploadfile/201603/9b4f1459313227.png)

现在Site Map中就有整理整齐的URL了：

[[![Burp Suite新手指南](images/img-012-b20df15072ba.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-72451459313278.png)](https://mrxn.net/content/uploadfile/201603/72451459313278.png)

Spider –> Options标签下有些你可以调整的选项，如user-agent ，或者爬虫应该爬多深，两个重要的设置是表单提交和应用登录，设置好之后爬虫可以自动为你填写表单：

[[![Burp Suite新手指南](images/img-013-76c17d6c1618.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-792b1459313321.png)](https://mrxn.net/content/uploadfile/201603/792b1459313321.png)

## Intruder

Intruder是Burp Suite中最受欢迎的工具。Intruder是获取Web应用信息的工具。它可以用来爆破，枚举，漏洞测试等任何你想要用的测试手段，然后从结果中获取数据。

网络安全

我举个例子来演示Intruder的使用方法。即爆破登录页面的管理员密码（假设没有帐号锁定）。首先，我们切换到Proxy-> HTTP History，右键要测试的请求，点击“Send To Intruder”：

[[![Burp Suite新手指南](images/img-014-0322787cc0df.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-275e1459313362.png)](https://mrxn.net/content/uploadfile/201603/275e1459313362.png)

接下来我们切换到Intruder标签，准备攻击。程序会在Target标签里自动填上请求中的host和端口。在Position（位置）标签出哦我们可以看到我们选择的请求并设置我们要攻击的位置。用鼠标高亮想要攻击的位置， 然后点击右边的“Add”，如果需要的话可以选择多个位置：

[[![Burp Suite新手指南](images/img-015-d9d2354d6603.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-7c341459313405.png)](https://mrxn.net/content/uploadfile/201603/7c341459313405.png)

最上面的地方有多种攻击类型，本例中我们使用默认的Sniper，但实际上每种攻击类型都有特定用途：

[blue]

代理与过滤

Sniper – 这个模式使用单一的payload组。它会针对每个位置设置payload。这种攻击类型适合对常见漏洞中的请求参数单独地进行fuzzing测试。攻击中的请求总数应该是position数量和payload数量的乘积。

Battering ram – 这一模式使用单一的payload组。它会重复payload并且一次把所有相同的payload放入指定的位置中。这种攻击适合那种需要在请求中把相同的输入放到多个位置的情况。请求的总数是payload组中payload的总数。

Pitchfork – 这一模式使用多个payload组。对于定义的位置可以使用不同的payload组。攻击会同步迭代所有的payload组，把payload放入每个定义的位置中。这种攻击类型非常适合那种不同位置中需要插入不同但相关的输入的情况。请求的数量应该是最小的payload组中的payload数量。

Cluster bomb – 这种模式会使用多个payload组。每个定义的位置中有不同的payload组。攻击会迭代每个payload组，每种payload组合都会被测试一遍。这种攻击适用于那种位置中需要不同且不相关或者未知的输入的攻击。攻击请求的总数是各payload组中payload数量的乘积。

[/blue]

位置设定好之后我们切换到Payloads标签，选择攻击时使用的数据。顶部的地方你可以看到payload组。各个组都对应设置的各个位置。我们可以选择payload类型，如简易列表(Simple List)。

计算机安全

在那下面有一些payload选项。每个payload类型都有不同的选项，供用户为你的测试进行修改。我经常使用的是数字(Numbers)，你可以设置范围，选择是连续的数字还是随机数字，还有每次攻击时的步长等。不过对于我们要搞的爆破攻击，我们只需要添加一个密码字典就行：

[[![Burp Suite新手指南](images/img-016-0a3eed5f193a.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-1a831459313491.png)](https://mrxn.net/content/uploadfile/201603/1a831459313491.png)

接下来就是点击右上角的开始攻击(Start Attack)按钮。程序就会弹出一个新的窗口，显示的是尝试的每个payload和响应的详情。我们的例子中，第六个请求获取到了正确的密码：

[[![Burp Suite新手指南](images/img-017-30effe9de539.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-38db1459313537.png)](https://mrxn.net/content/uploadfile/201603/38db1459313537.png)

我们返回主窗口，然后切换到Intruder –> Options标签页，可以发现还有些别配置。其中一个很重要的是“Grep– Match”功能，这个功能可以让你基于HTML中的字符串或者正则表达式标记出结果。这些标记会在新增的栏里出现。

[green]注：免费版的Burp Suite会对Intruder限速，专业版会更快。[/green]

漏洞修复方案

Repeater(重复器)、decoder(解码器)和comparer(比较器)也很有用，但由于使用简单，在此就不再赘述了。

原文地址：https://matttheripperblog.files.wordpress.com/2016/01/add-to-scope.png?w=770

工具下载地址：[渗透测试神器Burpsuite Pro v1.6.38（含下载）](https://mrxn.net/hacktools/burpsuite_pro_cracked_v1_6_38.html)

- 标签：
- [#渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
- [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
- [#SQL](https://mrxn.net/tag/SQL)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F)

---

文章目录

- [1.
  Intercepting Proxy（截取代理）](#toc-1-)
- [2.
  Spider（爬虫）](#toc-2-)
- [3.
  Intruder](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
