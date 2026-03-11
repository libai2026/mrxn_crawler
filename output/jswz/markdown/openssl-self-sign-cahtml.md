---
title: "基于OpenSSL自建CA和颁发SSL证书"
source: https://mrxn.net/jswz/openssl-self-sign-ca.html
---

# 基于OpenSSL自建CA和颁发SSL证书

[Mrxn](https://mrxn.net/author/1)* 发表于2015/9/24 22:13
* 12288浏览
* [2评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

关于SSL/TLS介绍见文章
[SSL/TLS原理详解](https://mrxn.net/tls-ssl-understand.html)
。
  
关于证书授权中心CA以及数字证书等概念，请移步
[OpenSSL 与 SSL 数字证书概念贴](https://mrxn.net/openssl-certificate-encryption.html)
。

openssl是一个开源程序的套件、这个套件有三个部分组成：一是
`libcryto`
，这是一个具有通用功能的加密库，里面实现了众多的加密库；二是
`libssl`
，这个是实现ssl机制的，它是用于实现TLS/SSL的功能；三是openssl，是个多功能命令行工具，它可以实现加密解密，甚至还可以当CA来用，可以让你创建证书、吊销证书。

默认情况ubuntu和CentOS上都已安装好openssl。CentOS 6.x 上有关ssl证书的目录结构：

```
/etc/pki/CA/
            newcerts    存放CA签署（颁发）过的数字证书（证书备份目录）
            private     用于存放CA的私钥
            crl         吊销的证书
/etc/pki/tls/
             cert.pem    软链接到certs/ca-bundle.crt
             certs/      该服务器上的证书存放目录，可以房子自己的证书和内置证书
                   ca-bundle.crt    内置信任的证书
             private    证书密钥存放目录
             openssl.cnf    openssl的CA主配置文件
```

# 1. 颁发证书

## 1.1 修改CA的一些配置文件

CA要给别人颁发证书，首先自己得有一个作为根证书，我们得在一切工作之前修改好CA的配置文件、序列号、索引等等。

**`vi /etc/pki/tls/openssl.cnf`**
：

```
...
[ CA_default ]
dir             = /etc/pki/CA           # Where everything is kept
certs           = $dir/certs            # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several ctificates with same subject.
new_certs_dir   = $dir/newcerts         # default place for new certs.
certificate     = $dir/cacert.pem       # The CA certificate
serial          = $dir/serial           # The current serial number
crlnumber       = $dir/crlnumber        # the current crl number
                                        # must be commented out to leave a V1 CRL
crl             = $dir/crl.pem          # The current CRL
private_key     = $dir/private/cakey.pem # The private key
RANDFILE        = $dir/private/.rand    # private random number file
...
default_days    = 3650                  # how long to certify for
...
# For the CA policy
[ policy_match ]
countryName             = match
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional
...
[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = CN
countryName_min                 = 2
countryName_max                 = 2
stateOrProvinceName             = State or Province Name (full name)
stateOrProvinceName_default     = GD
...
[ req_distinguished_name ] 部分主要是颁证时一些默认的值，可以不动
```

一定要注意
`[ policy_match ]`

中的设定的匹配规则，是有可能因为证书使用的工具不一样，导致即使设置了csr中看起来有相同的countryName,stateOrProvinceName等，但在最终生成证书时依然报错：

```
Using configuration from /usr/lib/ssl/openssl.cnf
Check that the request matches the signature
Signature ok
The stateOrProvinceName field needed to be the same in the
CA certificate (GuangDong) and the request (GuangDong)
```

**`touch index.txt serial`**

：
  
  

在CA目录下创建两个初始文件：

```
# touch index.txt serial
# echo 01 > serial
```

## 1.2 生成根密钥

```
# cd /etc/pki/CA/
# openssl genrsa -out private/cakey.pem 2048
```

为了安全起见，修改cakey.pem私钥文件权限为600或400，也可以使用子shell生成
`( umask 077; openssl genrsa -out private/cakey.pem 2048 )`
，下面不再重复。

## 1.3 生成根证书

使用req命令生成自签证书：

```
# openssl req -new -x509 -key private/cakey.pem -out cacert.pem
```

会提示输入一些内容，因为是私有的，所以可以随便输入（之前修改的openssl.cnf会在这里呈现），最好记住能与后面保持一致。上面的自签证书
`cacert.pem`
应该生成在
`/etc/pki/CA`
下。

## 1.4 为我们的nginx web服务器生成ssl密钥

以上都是在CA服务器上做的操作，而且只需进行一次，现在转到nginx服务器上执行：

```
# cd /etc/nginx/ssl
# openssl genrsa -out nginx.key 2048
```

这里测试的时候CA中心与要申请证书的服务器是同一个。

## 1.5 为nginx生成证书签署请求

```
# openssl req -new -key nginx.key -out nginx.csr
...
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:GD
Locality Name (eg, city) []:SZ
Organization Name (eg, company) [Internet Widgits Pty Ltd]:COMPANY
Organizational Unit Name (eg, section) []:IT_SECTION
Common Name (e.g. server FQDN or YOUR name) []:your.domain.com
Email Address []:
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
...
```

同样会提示输入一些内容，其它随便，除了
`Commone Name`
一定要是你要授予证书的服务器域名或主机名，challenge password不填。

## 1.6 私有CA根据请求来签署证书

接下来要把上一步生成的证书请求csr文件，发到CA服务器上，在CA上执行：

```
# openssl ca -in nginx.csr -out nginx.crt
另外在极少数情况下，上面的命令生成的证书不能识别，试试下面的命令：
# openssl x509 -req -in server.csr -CA /etc/pki/CA/cacert.pem -CAkey /etc/pki/CA/private/cakey.pem -CAcreateserial -out server.crt
```

上面签发过程其实默认使用了
`-cert cacert.pem -keyfile cakey.pem`
，这两个文件就是前两步生成的位于
`/etc/pki/CA`
下的根密钥和根证书。将生成的crt证书发回nginx服务器使用。

到此我们已经拥有了建立ssl安全连接所需要的所有文件，并且服务器的crt和key都位于配置的目录下，剩下的是如何使用证书的问题。

# 2. 使用ssl证书

## 2.1 一般浏览器

浏览器作为客户端去访问https加密的服务器，一般不用去手动做其他设置，如
`https://www.google.com.hk`
，这是因为Chrome、FireFox、Safari、IE等浏览器已经内置了大部分常用的CA的根证书，但自建CA的根证书就不再浏览器的信任列表中，访问时会提示如下：
  
IE浏览器

[![基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/content/uploadfile/201509/a6081443107850.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/a6081443107850.png)

谷歌浏览器
[![基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/content/uploadfile/201509/thum-87241443107850.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/87241443107850.png)

安装网站证书后（同时也有信任的根证书），地址栏一般会显示绿色小锁
[![基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/content/uploadfile/201509/12161443107930.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/12161443107930.png)

证书信息
[![基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/content/uploadfile/201509/thum-ee2c1443107850.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/ee2c1443107850.png)

导入证书到浏览器的方法：
<http://cnzhx.net/blog/self-signed-certificate-as-trusted-root-ca-in-windows/>

## 2.2 为linux系统添加根证书

这一步不是必须的，一般出现在开发测试环境中，而且具体的应用程序应该提供添加证书的方法。

`curl`
工具可以在linux上模拟发送请求，但当它去访问https加密网站时就会提示如下信息：

```
# curl https://sean:[email protected]:8000/
curl: (60) Peer certificate cannot be authenticated with known CA certificates
More details here: http://curl.haxx.se/docs/sslcerts.html
curl performs SSL certificate verification by default, using a "bundle"
 of Certificate Authority (CA) public keys (CA certs). If the default
 bundle file isn't adequate, you can specify an alternate file
 using the --cacert option.
If this HTTPS server uses a certificate signed by a CA represented in
 the bundle, the certificate verification probably failed due to a
 problem with the certificate (it might be expired, or the name might
 not match the domain name in the URL).
If you'd like to turn off curl's verification of the certificate, use
 the -k (or --insecure) option.
```

提示上面的信息说明curl在linux的证书信任集里没有找到根证书，你可以使用
`curl --insecure`

来不验证证书的可靠性，这只能保证数据是加密传输的但无法保证对方是我们要访问的服务。使用
`curl --cacert cacert.pem`

可以手动指定根证书路径。我们也可以把根证书添加到系统（CentOS 5,6）默认的bundle：
  

```
# cp /etc/pki/tls/certs/ca-bundle.crt{,.bak}    备份以防出错
# cat /etc/pki/CA/cacert.pem >> /etc/pki/tls/certs/ca-bundle.crt
# curl https://sean:[email protected]:8000
"docker-registry server (dev) (v0.8.1)"
```

## 2.3 nginx

在nginx配置文件（可能是
`/etc/nginx/sites-available/default`
）的server指令下添加：

  

```
ssl on;
ssl_certificate /etc/nginx/ssl/nginx.crt;
ssl_certificate_key /etc/nginx/ssl/nginx.key;
```

  

同时注意 server\_name 与证书申请时的 Common Name 要相同，打开443端口。当然关于web服务器加密还有其他配置内容，如只对部分URL加密，对URL重定向实现强制https访问，请参考其他资料。

# 3 关于证书申请

注意，如果对于一般的应用，管理员只需生成“证书请求”（后缀大多为.csr），它包含你的名字和公钥，然后把这份请求交给诸如verisign等有CA服务公司（当然，连同几百美金），你的证书请求经验证后，CA用它的私钥签名，形成正式的证书发还给你。管理员再在web server上导入这个证书就行了。如果你不想花那笔钱，或者想了解一下原理，可以自己做CA。从ca的角度讲，你需要CA的私钥和公钥。从想要证书的服务器角度将，需要把服务器的证书请求交给CA。

如果你要自己做CA，别忘了客户端需要导入CA的证书（CA的证书是自签名的，导入它意味着你“信任”这个CA签署的证书）。而商业CA的一般不用，因为它们已经内置在你的浏览器中了。

**参考**

* [CentOS6.5下openssl加密解密及CA自签颁发证书详解](http://blog.csdn.net/napolunyishi/article/details/42425827)
* [基于 OpenSSL 的 CA 建立及证书签发](http://www.cnblogs.com/popsuper1982/p/3843772.html)
* [openssl建立证书，非常详细配置ssl+apache](http://blog.51yip.com/apachenginx/958.html)
* [The Secure Sockets Layer and Transport Layer Security](http://www.ibm.com/developerworks/library/ws-ssl-security/)

原文地址：http://seanlook.com/2015/01/18/openssl-self-sign-ca/

* 标签：
* [#
  网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
* [#
  加密通讯](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86%E9%80%9A%E8%AE%AF)
* [#
  http](https://mrxn.net/tag/http)
* [#
  ssl](https://mrxn.net/tag/ssl)
* [#
  https](https://mrxn.net/tag/https)
* [#
  nginx](https://mrxn.net/tag/nginx)
* [#
  vps](https://mrxn.net/tag/vps)
* [#
  运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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
[基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/jswz/openssl-self-sign-ca.html)
  
文章链接：
<https://mrxn.net/jswz/openssl-self-sign-ca.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/openssl-self-sign-ca.html"),
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
text: encodeURI("https://mrxn.net/jswz/openssl-self-sign-ca.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});