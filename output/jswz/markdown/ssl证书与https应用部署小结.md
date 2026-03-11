---
title: "SSL证书与Https应用部署小结"
source: https://mrxn.net/jswz/https-apply-all.html
asset_dir: assets/ssl证书与https应用部署小结
---

# SSL证书与Https应用部署小结

[Mrxn](https://mrxn.net/author/1)* 发表于2015/9/24 22:51
* 8925浏览
* [4评论](#comment)
* 2小时阅读

深入探索

web服务器

代理

应用


(adsbygoogle = window.adsbygoogle || []).push({});

---

为了提高网站的安全性，一般会在比较敏感的部分页面采用https传输，比如注册、登录、控制台等。像Gmail、网银等全部采用https传输。

https/ssl 主要起到两个作用：网站认证、内容加密传输和数据一致性。经CA签发的证书才起到认证可信的作用，所有有效证书均可以起到加密传输的作用。

网络安全

**浏览器与SSL证书**

[![SSL应用部署小结 - hanguokai - 韩国恺的博客](images/img-001-c6497aeaea10.png)](https://mrxn.net/content/uploadfile/201509/b94e5ebe142beefe76c8737e9682c7e120150924155330.png)

上图是IE和Chrome上对https的不同表现。

Chrome 网站安全性指示器说明：[http://support.google.com/chrome/bin/answer.py?hl=zh&answer=95617](https://support.google.com/chrome/bin/answer.py?hl=zh&answer=95617)

SSL最主要应用是在浏览器和Web服务器之间，尽管不限于此。当然，安全本身是重要的内在属性。但在表面上看，部署SSL 就是为了让用户浏览器里看起来更安全一些，以增加用户的信任感。所以很多企业更把它当作门面，而签发机构也为此卖高价，尤其是国内的价格明显高于国外的。

实际上SSL证书也可以做客户端认证，用户拥有自己特有的证书，用它可以证明自己的身份，当然也就用不着用户名和密码了。但这种用的很少，一般web服务器也不支持。

内容加密传输更安全，如果只是为了加密，使用自签发的证书也可以，但浏览器无法验证证书，所以会给出一个非常吓人的警告，所以自签发证书不适合给外人使用，只适合内部使用，把这个证书 加入到自己的信任列表或忽略证书验证即可，以后就不会继续拦截了。

证书需要被少数一级或二级 CA 认证才有效。计算机安全中的信任就是一个信任链的关系，信任链最顶端的被称为根证书。

自签发的证书在技术上是完全一样的，仅用于加密传输是没问题的。但是不能被外人信任，所以一般仅用于内部使用。除了自签发不被信任，如果证书过期、已被吊销或者非证书所代表的域名也都是不被信任的，导致证书验证出错。

开发工具

用于网站的证书需要被大众信任，所以不能自签发的证书，那就申请（购买）一个吧。

**申请证书**

**1.证书类别**

按证书包含域名数量分为：

* 单域名：只针对这个域名有效，不能用在其它域名下。
* 多域名：只针对列出的多个域名有效。
* 通配符域名(wildcard)：对任意子域名有小，显示的是 \*.example.com。

注意：SSL所说的单个域名是一个完整的域名，一个子域名就算一个，而非一个顶级域名。

如果网站有很多子域名，只需要申请真正需要的域名证书。

按验证的类别分：

安全工具开发

* 域名认证（Domain Validation）：认证你的域名所有权和网站，申请验证简单，几分钟即可。
* 组织机构认证（Organization Validation）：认证的域名和公司信息，需要提交公司资料认证。
* 扩展认证（Extended Validation，简称EV）：这种证书会在浏览器中出现“很明显”的绿色地址栏，给用户的可信度最高。有安全评估保证。

个人或小站点可用一类或二类，企业一般用二类认证，少数企业会用到EV认证。

**2. 证书价格**

看了看网上SSL证书的价格，便宜的一般都是10美元左右一个子域名/每年，按不同类别、不同品牌等价格在几十美元到几百美元一年。比如能显示绿色地址栏的EV证书和通配符证书贵一些。国内自己的或[代理](#)的，比国外贵不少，动辄几千元。其实就是由可信源认证了一下，类似于办证，用起来没什么差别，并非越贵越好。

**3. 签发机构（“卖家”）**

[![SSL应用部署小结 - hanguokai - 韩国恺的博客](images/img-002-f067e57a9b41.png)](https://mrxn.net/content/uploadfile/201509/a9779fb9446d1a7a8ce8911a7c74511e20150924155331.png)

国外常见的SSL提供商有：Thawte，Go Daddy，VeriSign，RapidSSL，GeoTrust（QuickSSL），StartSSL，Comodo。

StartSSL、Go Daddy的比较便宜，GeoTrust、Comodo的价格适中，Thawte和VeriSign的价格较贵。

网络浏览器

VeriSign现在归属赛门铁克，在国内是由天威诚信代理的。世界真小，天威诚信就在我很多年以前的东家（启明星辰）大楼里，地下一层是他们的机房，我还进去过一次。

**4. 免费的StartSSL**

唯一免费的是StartSSL，其它的一般只提供30免费试用。

但 StartSSL 提供的免费证书是一类的、仅对域名和email进行验证，不对组织做验证（也就是面向自然人的，非面向组织机构的），不过

仅作为域名验证和数据加密也够了，并且浏览器也认它，一般人也不会去看你的证书级别。适合个人和初创网站使用，以后有钱了再申请个收费的替换即可。

我很顺利地申请到了免费的StartSSL证书，分别用在两个子域上。

网络安全

最后，证书签发给你后，最主要是保护好私钥证书，这个丢失或泄漏就完了。因为如果被别人利用也就毫无安全性了，需要向证书签发机构申请撤销证书并申请新的证书，这当然也是要收费的。

**应用规划、配置和调整**

并不是说有了SSL证书就没事了，还要考虑应用中的使用问题，需要规划、服务器配置、应用调整等多个环节。

SSL比 http 要消耗更多cpu资源（主要是在建立连接的阶段，之后还要对内容加密），所以对一般网站，只需要对部分地方采用https，大部分开放内容是没必要的，具体取决于你的业务要求。比如对于很多安全要求较低的网站，完全不用https也是可接受的。

**某些页面是同时支持 http 和 https ，还是只支持 https、强制 https？**

同时支持就是用户用什么协议访问都可以，那么用户的请求主要就是由页面本身的链接引导来的，因为一般用户不会自己特意去修改地址栏的。

网站托管与域名注册

一般我们的网站可以做成同时支持http和https，都可以访问。但是这就容易有后面说的混合内容或混合脚本的问题。

还可以规划为部分页面支持 https，一般公开页面不用https，只是将部分地方的链接改为 https 就可以了。专门期望以 https 访问的页面中，引用的绝对URL可以明确的使用 https链接。

是否强制 https ？对于安全性高的网站或网站中的部分页面，可以强制使用https访问， 即使用户在地址栏里手工把 https 改为 http， 也会被自动重定向回 https 上。比如可以通过配置web服务器 rewrite 规则将这些 http url 自动重定向到对应的 https url 上（这样维护比较简单），而不用改应用。

**解决混合内容问题(****http和https)**

混合内容是指：在https的页面中混合了非https的资源请求，比如图片、css、js 等等。如果是混合了非 https 的 js 代码，则被称为混合脚本。

安全工具开发

混合内容的危害：如果只是混合了不安全的图片和css，那么受中间人攻击篡改，一般只会影响页面的显示，危害相对小一点。如果是混合了不安全的 js 代码，则这个不安全的 js 可以完全访问和修改页面中的任何内容，这是非常危险的。

另请参看，Chrome对混合脚本危害的说明与提示：[Trying to end mixed scripting vulnerabilities](https://googleonlinesecurity.blogspot.com/2011/06/trying-to-end-mixed-scripting.html)

所以，只有页面本身和所有引用的资源都是 https 的浏览器才认为是安全的，只要其中引用了非安全资源（即使图片），浏览器都会给出**不安全**的提示，特别是有 js 的情况。如果浏览器提示不安全，那样我们就达不到原来目的了。我们费了半天功夫去申请 SSL 证书，配置Web服务器，最后如果因为混合内容而前功尽弃就太糟了。咱继续努力吧，想办法让所有引用资源都是安全的。

理论上，混合了第三方的内容，即使是SSL的第三方内容也不是很好。因为用户信任的是你，而不是第三方，即使第三方也支持https，但你能保证第三方就绝对安全吗。不引用任何第三方才是绝对安全的，但这样太严格了，安全其实也是一个 tradeoff 的问题，需要考虑很多方面的平衡。还好，起码现在浏览器认为已经是安全的了。

**引用第三方文件的问题（如 CDN 分发的文件）**

简单地说，这个问题要么有第三方提供 https 支持，要么不用它（用自己本地的）。

代理与过滤

一般我们会引用由 CDN 分发的文件，比如某个 js 库文件，而不用访问自己网站上的，这样借助 CDN 网络可以加快速度，这当然很好。

但是，如果我们在页面中使用绝对 URL 直接引用这个文件就无法自动使用 https 了！出现了混合协议内容，浏览器又该“变脸”了。

当SSL 遇上CDN 或 其它第三方文件就有点麻烦，因为很多CDN还不支持SSL。如果支持 https 的话就可以直接用 https 的绝对URL了，即使是同时支持http 和 https 的页面，这样做也不算太浪费，起码解决了问题。

因为CDN的云文件提供者，一般为每个cdn用户创建一个单独的子域名来使用，这样的话，CDN提供者要想支持 https 就必须支持所有可能的子域名，因此要求CDN提供方使用那种通配符子域名的证书。

**相对 URL、绝对 URL 与 只缺协议的URL(****Protocol Relative URL****)**

相对路径比较简单，自动匹配用户请求的 http 或 https 协议。

但是绝对 url 则不成，因为绝对 url 已经明确地写上了协议： http://www.example.com/jquery.js 。

这个问题还有一个办法解决，你一定没见过这种形式：**//www.example.com/jquery.js**

哈哈，一个缺少协议的URL（实际上还算是相对URL），这种形式可以在浏览器中被正确补充上合适的协议！很多人都用这种方法。

但是，这里有点小问题，IE7 和 IE8 处理这种缺少协议的URL的css 文件时，同一个css文件会下载两次，详见[Steve的文章](http://www.stevesouders.com/blog/2010/02/10/5a-missing-schema-double-download/) 。

**JS 自动判断当前协议**

现在我们经常用 js 来加载其它 js 文件或 其它别的文件，如果是请求是相对URL则没问题，如果是绝对URL怎么办？

网络浏览器

其实 js 脚本可以这样：**document.location.protocol** 等于 'http:' 还是 'https:' 来判断。例如在 Google Analytics 的嵌入代码中：

ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';

**应用程序中如何判断访问协议**

对于动态页面，如 jsp、php等，也是可以动态判断当前是否使用了 https 协议的。所以应用可以根据动态判断，来生成不同的引用 URL。这样虽然有点麻烦，但也算是解决了自动识别协议的问题，当然相对路径总是不需要处理的。

比如在 jsp 中：

* request.isSecure() 为true 表示当前为 https ，false表示 http 访问
* request.getScheme() 返回字符串 https 或 http

注意，如果 tomcat 部署在其它web服务器[代理](#)的后面，需要正确配置好才能返回正确结果，见本文最后一部分。

**同源策略的问题**

最后提醒一点：http 和 https是不同源的！即使后面的内容都一样。所以 ajax 发请求的时候要使用正确协议的绝对URL才行。

相对URL的 ajax 请求没关系。

网络安全

**Nginx 配置**

小结一下 Nginx 配置SSL注意的问题，详细安装配置内容请参考其它资料，如官方 [SSL模块](http://wiki.nginx.org/HttpSslModule) 和 [https配置文档](http://nginx.org/en/docs/http/configuring_https_servers.html)。

**1. 首先检查一下是否已安装了 SSL模块**，因为默认是不包含的。

用 nginx -V 命令检查一下。如果没有ssl模块则需要重新安装（建议升级到最新版本），注意安装时加上ssl 选项：

./configure --with-http\_ssl\_module

另外，nginx需要依赖 openssl 提供ssl支持，这个也要有。

网站托管与域名注册

**2. nginx.conf 中的典型配置示例**

listen     80;

listen    443 ssl;

ssl\_certificate      cert.pem; #修改具体文件

ssl\_certificate\_key  ssl.key; #修改具体文件

ssl\_session\_cache    shared:SSL:10m;

ssl\_session\_timeout  10m;

ssl\_protocols  SSLv2 SSLv3 TLSv1;

ssl\_ciphers  ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;

ssl\_prefer\_server\_ciphers   on;

上面第2-4项是关键。这些配置放在 server 块就可以对其中的所有 location 生效了，并且同时支持 http 和 https 。或者把 http 和 https 分开配置也很常见。

**3. 合并证书配置文件**

和Apache配置不同，Nginx需要将服务器证书和ca证书链合并到一个文件中，作为 ssl\_certificate 配置的内容。

安全工具开发

例如，按照证书链从下向上的顺序，我有三个证书：

1. ssl.crt（自己域名的服务器证书）
2. sub.class1.server.ca.pem（startssl 的一类证书）
3. ca.pem（startssl 的根证书）

把它们的内容按顺序连接到的一个文件中，每个内容另起一行，中间没有空行或空格。

**4. 避免启动时输入密码**

配好之后，启动nginx 要你输入密钥的密码。这是因为 ssl\_certificate\_key 配置对应的文件（也就是 startssl 给你的私钥文件）内容是加密的，需要输入你创建这个时设置的密码才能解密。这样私钥虽然很安全，但是每次重启服务都要输入一次密码也太麻烦了。其实，只要证书改为解密了的内容，就可以避免每次输入密码。用如下命令即可：

openssl rsa -in ssl.key -out newssl.key  输入密码，就生成了解密后的私钥内容，使用这个就OK了。

开发工具

但是就像前面说的，一定要在服务器上保护好它，例如：

chmod 400 ssl.key （仅root可读）

**5. 优化SSL配置**

SSL 很消耗 CPU 资源，尤其是在建立连接的握手阶段。一是通过开启 keepalive 可以重用连接。二是可以重用和共享ssl session，见上面ssl\_session相关配置。

**独立Tomcat+SSL**

Tomcat 是很常见的 Java应用服务器，当然也可以作为独立的 Web服务器，所有用户请求直接访问 tomcat。

代理与过滤

如果 Tomcat 作为独立的Web服务器，那么就需要配置Tomcat就可以了，文档参考[这里](http://tomcat.apache.org/tomcat-6.0-doc/ssl-howto.html) 和 [这个](http://tomcat.apache.org/tomcat-6.0-doc/config/http.html#SSL_Support)。主要是配置存放证书的 Keystore 和 连接器Connector。

**Java的keystore**

keystore 是 Java 中专用并内置的一个类似于 openssl 的工具，一个 keystore 文件就是一个“保险箱”（database），专门存放证书和密钥，和相关的管理功能：生成自签发的证书、密钥、导入导出等。可以通过 keytool 命令或 Java api 交互。

利用keytool 命令将你的证书导入进去。

**Tomcat中Connector**

tomcat中有三种 Connector 实现：block、nio 和 APR。前两者使用Java SSL（这需要 keystore 的配置 ），APR使用OpenSSL（不需要用keystore，直接指定证书），配置略有不同。

网络安全

**Nginx+Tomcat+SSL**

实际上，大规模的网站都有很多台Web服务器和应用服务器组成，用户的请求可能是经由 Varnish、HAProxy、Nginx之后才到应用服务器，中间有好几层。而中小规模的典型部署常见的是 Nginx+Tomcat 这种两层配置，而Tomcat 会多于一台，Nginx 作为静态文件处理和负载均衡。

如果Nginx作为前端[代理](#)的话，则Tomcat根本不需要自己处理 https，全是Nginx处理的。用户首先和Nginx建立连接，完成SSL握手，而后Nginx 作为代理以 http 协议将请求转给 tomcat 处理，Nginx再把 tomcat 的输出通过SSL 加密发回给用户，这中间是透明的，Tomcat只是在处理 http 请求而已。因此，这种情况下不需要配置 Tomcat 的SSL，只需要配置 Nginx 的SSL 和 Proxy。

安全工具开发

**在代理模式下，Tomcat 如何识别用户的直接请求（URL、IP、https还是http )？**

在透明代理下，如果不做任何配置Tomcat 认为所有的请求都是 Nginx 发出来的，这样会导致如下的错误结果：

* request.getScheme()  //总是 http，而不是实际的http或https
* request.isSecure()  //总是false（因为总是http）
* request.getRemoteAddr()  //总是 nginx 请求的 IP，而不是用户的IP
* request.getRequestURL()  //总是 nginx 请求的URL 而不是用户实际请求的 URL
* response.sendRedirect( 相对url )  //总是重定向到 http 上 （因为认为当前是 http 请求）

如果程序中把这些当实际用户请求做处理就有问题了。解决方法很简单，只需要分别配置一下 Nginx 和 Tomcat 就好了，而不用改程序。

配置 Nginx 的转发选项：

proxy\_set\_header       Host $host;

proxy\_set\_header  X-Real-IP  $remote\_addr;

proxy\_set\_header  X-Forwarded-For $proxy\_add\_x\_forwarded\_for;

proxy\_set\_header X-Forwarded-Proto  $scheme;

配置Tomcat server.xml 的 Engine 模块下配置一个 Value：

网站托管与域名注册

<Valve className="org.apache.catalina.valves.RemoteIpValve" remoteIpHeader="X-Forwarded-For" protocolHeader="X-Forwarded-Proto" protocolHeaderHttpsValue="https"/>

配置双方的 X-Forwarded-Proto 就是为了正确地识别实际用户发出的协议是 http 还是 https。X-Forwarded-For 是为了获得实际用户的 IP。

这样以上5项测试就都变为正确的结果了，就像用户在直接访问 Tomcat 一样。

原文地址：http://han.guokai.blog.163.com/blog/static/136718271201211631456811/

网络安全

* 标签：
* [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
* [#加密通讯](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86%E9%80%9A%E8%AE%AF)
* [#ssl](https://mrxn.net/tag/ssl)
* [#https](https://mrxn.net/tag/https)
* [#nginx](https://mrxn.net/tag/nginx)
* [#vps](https://mrxn.net/tag/vps)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[SSL证书与Https应用部署小结](https://mrxn.net/jswz/https-apply-all.html)  
文章链接：<https://mrxn.net/jswz/https-apply-all.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/https-apply-all.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/https-apply-all.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 