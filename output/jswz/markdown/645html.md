---
title: "寻找CDN背后的真实IP方式总结之2019完结篇"
source: https://mrxn.net/jswz/645.html
---

# 寻找CDN背后的真实IP方式总结之2019完结篇

[Mrxn](https://mrxn.net/author/1)* 发表于2019/10/30 05:35
* 5014浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

注：总共两篇文章，第一篇文章来自信安，第二篇来自 WhITECat。我这里只是总结一下，方便自己查看，不用每次都去翻好几篇文章，如果两位原作不允许，随时删除。
  
  
第一篇：绕过
[CDN](https://mrxn.net/tag/cdn)
寻找真实 IP 地址的各种姿势
  
  
个人觉得，绕过
[CDN](https://mrxn.net/tag/cdn)
去寻找主机的真实 ip，更容易能寻找到企业网络的薄弱地带，所以 Bypass
[CDN](https://mrxn.net/tag/cdn)
也就变成了至关重要的一点。
  
  
0x01 常见 Bypass 方法
  
  
域名搜集
  
  
由于成本问题，可能某些厂商并不会将所有的子域名都部署
[CDN](https://mrxn.net/tag/cdn)
，所以如果我们能尽量的搜集子域名，或许可以找到一些没有部署
[CDN](https://mrxn.net/tag/cdn)
的子域名，拿到某些服务器的真实 ip/ 段
  
  
然后关于子域名搜集的方式很多，就不一一介绍了，我平时主要是从这几个方面搜集子域名：
  
  
1、SSL 证书
  
  
2、爆破
  
  
3、Google Hacking
  
  
4、同邮箱注册人
  
  
4、DNS 域传送
  
  
5、页面 JS 搜集
  
  
6、网络空间引擎
  
  
  
  
工具也有很多厉害的，平时我一般使用 OneForALL + ESD + JSfinder 来进行搜集，（ESD 可以加载 layer 的字典，很好用）
  
  
  
  
查询 DNS 历史解析记录
  
  
常常服务器在解析到
[CDN](https://mrxn.net/tag/cdn)
服务前，会解析真实 ip，如果历史未删除，就可能找到
  
  
常用网站：
  
  
  
  
<http://viewdns.info/>
  
  
<https://x.threatbook.cn/>
  
  
<http://www.17ce.com/>
  
  
<https://dnsdb.io/zh-cn/>
  
  
<https://securitytrails.com/>
  
  
<http://www.ip138.com/>
  
  
<https://github.com/vincentcox/bypass-firewalls-by-DNS-history>
  
  
MX 记录（邮件探测）
  
  
这个很简单，如果目标系统有发件功能，通常在注册用户/找回密码等地方，通过注册确认、验证码等系统发来的邮件进行查看邮件原文即可查看发件IP地址。
  
  
SSL 证书探测
  
  
我们可以利用空间引擎进行 SSL 证书探测
  
  
443.https.tls.certificate.parsed.extensions.subject\_alt\_name.dns\_names:www.baidu.com
  
  
再放一个搜集证书的网站:
  
  
  
  
<https://crt.sh>
  
  
一个小脚本，可以快速搜集证书

# - *- coding: utf-8 -* -

# @Time    : 2019-10-08 22:51

# @Author  : Patrilic

# @FileName: SSL\_subdomain.py

# @Software: PyCharm

import requests
  
  
import re
  
  
  
  
TIME\_OUT = 60
  
  
def get\_SSL(domain):
  
  
domains = []
  
  
url = '
<https://crt.sh/?q=%25.{}'.format(domain>
)
  
  
response = requests.get(url,timeout=TIME\_OUT)
  
  
# print(response.text)
  
  
ssl = re.findall("<TD>(.\*?).{}</TD>".format(domain),response.text)
  
  
for i in ssl:
  
  
i += '.' + domain
  
  
domains.append(i)
  
  
print(domains)
  
  
  
  
if
**name**
== '
**main**
':
  
  
get\_SSL("baidu.com")
  
  
  
  
还有一种方式，就是搜集 SSL 证书 Hash，然后遍历 ip 去查询证书 hash，如果匹配到相同的，证明这个 ip 就是那个 域名同根证书的服务器真实 ip
  
  
简单来说，就是遍历 0.0.0.0/0:443，通过 ip 连接 https 时，会显示证书
  
  
当然，也可以用 censys 等引擎
  
  
偏远地区服务器访问
  
  
在偏远地区的服务器访问时，可能不会访问到
[CDN](https://mrxn.net/tag/cdn)
节点，而是直接访问服务器真实 ip
  
  
所以我们可以搞一个偏远地区的代理池，来访问目标域名，有概率就可以拿到真实 ip
  
  
也就是平常说的多地 Ping
  
  
favicon\_hash 匹配
  
  
利用 shodan 的 http.favicon.hash 语法，来匹配 icon 的 hash 值, 直接推:
  
  
<https://github.com/Ridter/get_ip_by_ico/blob/master/get_ip_by_ico.py>
  
  
CloudFlare Bypass
  
  
免费版的 cf，我们可以通过 DDOS 来消耗对方的流量，只需要把流量打光，就会回滚到原始 ip
  
  
还有利用 cloudflare 的改 host 返回示例:
  
  
<https://blog.detectify.com/2019/07/31/bypassing-cloudflare-waf-with-the-origin-server-ip-address/>
  
  
里面给了详细的介绍，我们可以通过 HOST 来判断是否是真实 ip, 具体看文章即可
  
  
奇特的 ping
  
  
比如可能有些地方，使用的
[CDN](https://mrxn.net/tag/cdn)
都是以 www.xxx.edu.cn，例如 www.cuit.edu.cn,www.jwc.cuit.edu.cn
  
  
可能去掉前缀的 www，就可能绕过 CDN 了，猜测应该是类似于 Apache VirtualHost, 可参考
  
  
<https://httpd.apache.org/docs/2.4/en/vhosts/examples.html>
  
  
例如对WWW域名和根域名(不带WWW)分别进行PING，结果有可能不同。
  
  
其实是 ping 了 www.xxx.xxx.cn 和 xxx.xxx.cn，这样就可以绕过 CDN 的检测。
  
  
利用老域名
  
  
在换新域名时，常常将 CDN 部署到新的域名上，而老域名由于没过期，可能未使用 CDN，然后就可以直接获取服务器真实 ip。
  
  
例如 patrilic.top > patrilic.com
  
  
域名更新时，可能老域名同时解析到真实服务器，但是没有部署 CDN
  
  
这个可以通过搜集域名备案的邮箱去反查，可能会有意外收获
  
  
暴力匹配
  
  
找到目标服务器 IP 段后，可以直接进行暴力匹配 ，使用 masscan 扫描 HTTP banner，然后匹配到目标域名的相同 banner
  
  
最后是 DDos/ 社工 CDN 平台等
  
  
0x02 其他方法
  
  
phpinfo.php 这类探针
  
  
ssrf，文件上传等漏洞
  
  
略..
  
  
  
  
第二篇文章：“最后”的Bypass CDN 查找网站真实IP
  
  
注：其实与第一篇有重复的的地方，请自行斟酌查看。
  
  
0x00起源~
  
  
查找网站真实IP过程中我们会经常用到一些Bypass CDN的手法，而Bypass CDN的常见姿势，之前看到过“信安之路”的某位大佬总结的挺好的，于是和小伙伴们又专门的去学习了一波，然后决定将学习心得归结于文字，以便于记录和复习。
  
  
0x01判断是否存在CDN
  
  
查找网站真实IP的第一步是先查看当前站点是否部署了CDN，而较为简单快捷的方式就是通过本地Nslookup查询目标站点的DNS记录，若存在CDN，则返回CDN服务器的地址，若不存在CDN,则返回的单个IP地址，我们认为它就是目标站点的真实IP。
  
  
除了使用nslookup，还可以通过第三方站点的DNS解析记录或者多地ping的方式去判断是否存在CDN。判断CDN只是个开始，不加赘述。。。
  
  
小伙伴-胡大毛的www法
  
  
以前用CDN的时候有个习惯，只让WWW域名使用cdn，秃域名不适用，为的是在维护网站时更方便，不用等cdn缓存。所以试着把目标网站的www去掉，ping一下看ip是不是变了，您别说，这个方法还真是屡用不爽。
  
  
小伙伴-刘正经的二级域名法
  
  
目标站点一般不会把所有的二级域名放cdn上，比如试验性质的二级域名。Google site一下目标的域名，看有没有二级域名出现，挨个排查，确定了没使用cdn的二级域名后，本地将目标域名绑定到同ip，能访问就说明目标站与此二级域名在同一个服务器上。不在同一服务器也可能在同C段，扫描C段所有开80端口的ip，挨个试。如果google搜不到也不代表没有，我们拿常见的二级域名构造一个字典，猜出它的二级域名。比如mail、cache、img。
  
  
查询子域名工具：layer子域名挖掘机 subdomin
  
  
扫描c段好用工具：zmap(
<https://www.cnblogs.com/China-Waukee/p/9596790.html>
)
  
  
还是“刘正经”的nslookup法
  
  
查询域名的NS记录，其域名记录中的MX记录，TXT记录等很有可能指向的是真实ip或同C段服务器。
  
  
注：域名解析--什么是A记录、别名记录(CNAME)、MX记录、TXT记录、NS记录（
<https://www.22.cn/help_34.html>
）
  
  
  
  
小伙伴-胡小毛的工具法
  
  
这个工具http://toolbar.netcraft.com据说会记录网站的ip变化情况，通过目标网站的历史ip地址就可以找到真实ip。没亲自测试，想必不是所有的网站都能查到。
  
  
例：
<http://toolbar.netcraft.com/site_report?url=http://www.waitalone.cn>
  
  
  
  
小伙伴-狄弟弟的目标敏感文件泄露
  
  
也许目标服务器上存在一些泄露的敏感文件中会告诉我们网站的IP,另外就是如phpinfo之类的探针。
  
  
  
  
小伙伴-匿名H的墙外法
  
  
很多国内的CDN没有节点对国外服务，国外的请求会直接指向真实ip。有人说用国外NS和或开国外VPN，但这样成功率太低了。我的方法是用国外的多节点ping工具，例如just-ping，全世界几十个节点ping目标域名，很有可能找到真实ip。
  
  
域名：
<http://www.just-ping.com/>
  
  
  
  
小伙伴-不靠谱的从CDN入手法
  
  
无论是用社工还是其他手段，反正是拿到了目标网站管理员在CDN的账号了，此时就可以自己在CDN的配置中找到网站的真实IP了。此法着实适用于“小伙伴-不靠谱”使用。
  
  
  
  
还是“不靠谱”的钓鱼法
  
  
不管网站怎么
[CDN](https://mrxn.net/tag/cdn)
，其向用户发的邮件一般都是从自己服务器发出来的。以wordpress为例，假如我要报复一个来我这捣乱的坏蛋，坏蛋使用了
[CDN](https://mrxn.net/tag/cdn)
，我要找到它的真实ip以便DDOS他。我的方法是在他博客上留言，再自己换个名回复自己，然后收到他的留言提醒邮件，就能知道发邮件的服务器ip 了。如果他没开提醒功能，那就试试他是不是开启了注册功能，wordpress默认是用邮件方式发密码的。
  
  
  
  
0x03“最后”的总结
  
  
小伙伴“最后”来了一波总结：
  
  
  
  
百因必有果，你的报应就是我~o~
  
  
  
  
万剑归宗不是火，万法合一才是果~o~
  
  
  
  
小伙伴们总结了一波又一波方法，“最后”表示不太行，方法很多，每一个看起来都很实用，但实战告诉我们，只有把这些方法都灵活贯通的结合使用才能达到最大的效果。“最后”以胡大毛的www法结合查找网站历史DNS解析记录的方法查找某个站点的真实IP的举例如下：
  
  
  
  
某站点www.xxx.com的当前解析显示有多个IP，但历史解析仅有一个IP，可以猜测该IP可能是真实IP。
  
  
  
  
“最后”认为除了需要将方法结合使用之外，辅助工具也是不可缺少的，于是又整理了一波常用的工具和查询平台如下：
  
  
  
  
1、查询SSL证书或历史DNS记录
  
  
  
  
<https://censys.io/certificates/&nbsp>
;  ###通过SSL证书查询真实IP（推荐）
  
  
  
  
<https://site.ip138.com/&nbsp>
;  ###DNS、IP等查询
  
  
  
  
<http://ping.chinaz.com/&nbsp>
;  ###多地ping
  
  
  
  
<http://ping.aizhan.com/&nbsp>
;  ###多地ping
  
  
  
  
<https://myssl.com/dns_check.html#dns_check&nbsp>
;  ###DNS查询
  
  
  
  
<https://securitytrails.com/&nbsp>
;  ### DNS查询
  
  
  
  
<https://dnsdb.io/zh-cn/&nbsp>
;   ###DNS查询
  
  
  
  
<https://x.threatbook.cn/&nbsp>
;  ###微步在线
  
  
  
  
<http://toolbar.netcraft.com/site_report?url=&nbsp>
;  ###在线域名信息查询
  
  
  
  
<http://viewdns.info/&nbsp>
;  ###DNS、IP等查询
  
  
  
  
<https://tools.ipip.net/cdn.php&nbsp>
;  ###CDN查 询IP
  
  
  
  
2、相关工具
  
  
  
  
子域名查询工具：layer子域名挖掘机，dirbrute，Oneforal（下载链接：
<https://github.com/shmilylty/OneForAll，推荐>
）
  
  
  
  
站点banner信息获取：Zmap，masscan等。
  
  
  
  
参考链接
  
  
<https://github.com/shmilylty/OneForAll>
  
  
  
  
<https://github.com/FeeiCN/ESD>
  
  
  
  
<https://github.com/Threezh1/JSFinder>
  
  
  
  
<https://github.com/AI0TSec/blog/issues/8>
  
  
  
  
<https://www.4hou.com/tools/8251.html>
  
  
  
  
<https://www.freebuf.com/sectool/112583.html>

* 标签：
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

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
[寻找CDN背后的真实IP方式总结之2019完结篇](https://mrxn.net/jswz/645.html)
  
文章链接：
<https://mrxn.net/jswz/645.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/645.html"),
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
text: encodeURI("https://mrxn.net/jswz/645.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});