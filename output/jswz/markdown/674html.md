---
title: "OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换"
source: https://mrxn.net/jswz/674.html
---

# OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换

[Mrxn](https://mrxn.net/author/1)* 发表于2020/9/2 01:07
* 6154浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

事件起因是我想听的歌曲，在网抑云听不了，我都开了VIP，还是由于版权原因，听不了。。。我难道要每一家都去开vip吗？同时开通每一家的VIP？没那个精力和金钱！那就用路由器搞起来！
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/7b111599037558.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/7b111599037558.png)
  
  
打开路由器发现解锁音乐的插件是关闭的，我打开后发现没起作用不说，正常的歌曲也打不开了，
  
  
打开music.163.com发现证书错误：
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-4f0f1599037558.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/4f0f1599037558.png)
  
  
我这个是由于我前一天没更新插件之前，已经手动替换过证书了可以使用了，当时也是证书错误，提示的是证书过期了。。。
  
  
前一天的证书替换过程参考如下：

```
➜  ~ openssl genrsa -out ca.key 2048
Generating RSA private key, 2048 bit long modulus
..............................+++
..............................................................+++
e is 65537 (0x10001)
➜  ~ openssl req -x509 -new -nodes -key ca.key -sha256 -days 1825 -out ca.crt -subj "/C=CN/CN=UnblockNeteaseMusic Root CA/O=netmusic"
➜  ~ openssl genrsa -out server.key 2048
Generating RSA private key, 2048 bit long modulus
.....................................+++
.....................+++
e is 65537 (0x10001)
➜  ~ openssl req -new -sha256 -key server.key -out server.csr -subj "/C=CN/L=Hangzhou/O=NetEase (Hangzhou) Network Co., Ltd/OU=IT Dept./CN=*.music.163.com"
➜  ~ openssl x509 -req -extfile <(printf "extendedKeyUsage=serverAuth\nsubjectAltName=DNS:music.163.com,DNS:*.music.163.com") -sha256 -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
Signature ok
subject=/C=CN/L=Hangzhou/O=NetEase (Hangzhou) Network Co., Ltd/OU=IT Dept./CN=*.music.163.com
Getting CA Private Key
➜  ~ ls
Applications               Public
Applications (Parallels)   Virtual Machines.localized
Desktop                    WeChatExtension-ForMac
Documents                  ca.crt
Downloads                  ca.key
Library                    ca.srl
Movies                     iCloud云盘（归档）
Music                      server.crt
Parallels                  server.csr
Pictures                   server.key
➜  ~ pwd
```

将server.crt server.key 替换掉,路径如下

```
root@OpenWrt:~# ls -l /usr/share/UnblockNeteaseMusicGo
-rw-r--r--    1 root     root          1675 Aug 31 13:10 ca.key
-rw-r--r--    1 root     root          1281 Aug 31 13:10 server.crt
-rw-r--r--    1 root     root          1679 Aug 31 13:10 server.key
root@OpenWrt:~#
```

再把ca.crt 安装到本机并信任就OK。
  
  
下面说一下如何更新插件，我是自己编译的插件，已经打包在GitHub仓库了，可以自己下载，链接放在最后。
  
  
你可以通过路由后台的文件上传或者是手动使用scp或者其他工具将插件上传到/tmp/目录，然后使用dpkg install 插件包名 来安装更新。我这个固件本身后台有文件上传：
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-b69b1599037558.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/b69b1599037558.png)
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-d77b1599037558.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/d77b1599037558.png)
  
  
上传完毕，就可以自行安装了。安装更新后就可以去网易云音乐解锁那个界面下载ca证书，然后本地安装，信任：
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-849d1599037559.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/849d1599037559.png)
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-de761599037559.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/de761599037559.png)
  
  
搞定后，打开网易云官网，查看证书，就是我们自己的证书，都OK了
  
  
[![OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/content/uploadfile/202009/thum-b0b31599037559.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/b0b31599037559.png)
  
  
  
  
编译备份插件文件列表：

```
编译时间:2020/09/01
.
├── brcmfmac-firmware-usb_20200619-1_arm_cortex-a9.ipk
├── busybox_1.31.1-2_arm_cortex-a9.ipk
├── ca-certificates_20200601-1_all.ipk
├── coremark_2020-05-28-7685fd32-15_arm_cortex-a9.ipk
├── ddns-scripts_aliyun_1.0.3-1_all.ipk
├── ddns-scripts_dnspod_1.0.2-1_all.ipk
├── default-settings_2-3_all.ipk
├── dns2socks_2.1-1_arm_cortex-a9.ipk
├── dnsmasq-full_2.81-7_arm_cortex-a9.ipk
├── dropbear_2020.80-1_arm_cortex-a9.ipk
├── firewall_2019-11-22-8174814a-1_arm_cortex-a9.ipk
├── getrandom_2019-12-31-0e34af14-4_arm_cortex-a9.ipk
├── hostapd-common_2020-06-08-5a8b3662-4_arm_cortex-a9.ipk
├── ip-full_5.7.0-2_arm_cortex-a9.ipk
├── ipset_7.4-1_arm_cortex-a9.ipk
├── ipt2socks_1.1.3-1_arm_cortex-a9.ipk
├── iptables-mod-fullconenat_2019-10-21-0cf3b48f-3_arm_cortex-a9.ipk
├── iw_5.4-1_arm_cortex-a9.ipk
├── jshn_2020-05-25-66195aee-1_arm_cortex-a9.ipk
├── jsonfilter_2018-02-04-c7e938d6-1_arm_cortex-a9.ipk
├── k3screenctrl_0.10-2_arm_cortex-a9.ipk
├── k3wifi_1-2_arm_cortex-a9.ipk
├── libblobmsg-json_2020-05-25-66195aee-1_arm_cortex-a9.ipk
├── libelf1_0.179-1_arm_cortex-a9.ipk
├── libevent2-7_2.1.11-2_arm_cortex-a9.ipk
├── libipset13_7.4-1_arm_cortex-a9.ipk
├── libjson-c4_0.13.1-2_arm_cortex-a9.ipk
├── libjson-script_2020-05-25-66195aee-1_arm_cortex-a9.ipk
├── liblua5.1.5_5.1.5-7_arm_cortex-a9.ipk
├── libmbedtls12_2.16.7-1_arm_cortex-a9.ipk
├── libmnl0_1.0.4-2_arm_cortex-a9.ipk
├── libnl-tiny_2019-10-29-0219008c-1_arm_cortex-a9.ipk
├── libopenssl1.1_1.1.1g-1_arm_cortex-a9.ipk
├── libopenssl-conf_1.1.1g-1_arm_cortex-a9.ipk
├── libpcre_8.44-2_arm_cortex-a9.ipk
├── libubox20191228_2020-05-25-66195aee-1_arm_cortex-a9.ipk
├── libubus20191227_2020-02-05-171469e3-1_arm_cortex-a9.ipk
├── libubus-lua_2020-02-05-171469e3-1_arm_cortex-a9.ipk
├── libuci_2018-08-11-4c8b4d6e-2_arm_cortex-a9.ipk
├── libuci-lua_2018-08-11-4c8b4d6e-2_arm_cortex-a9.ipk
├── libuclient20160123_2020-06-17-c6609861-1_arm_cortex-a9.ipk
├── libustream-openssl20200215_2020-03-13-5e1bc342-1_arm_cortex-a9.ipk
├── libuuid1_2.35.1-2_arm_cortex-a9.ipk
├── logd_2019-12-31-0e34af14-4_arm_cortex-a9.ipk
├── lua_5.1.5-7_arm_cortex-a9.ipk
├── luci-app-accesscontrol_1-11_all.ipk
├── luci-app-arpbind_1-3_all.ipk
├── luci-app-autoreboot_1.0-8_all.ipk
├── luci-app-cpufreq_1-5_all.ipk
├── luci-app-filetransfer_1-2_all.ipk
├── luci-app-ramfree_1.0-1_all.ipk
├── luci-app-sfe_1.0-13_all.ipk
├── luci-app-ttyd_1.0-3_all.ipk
├── luci-app-unblockmusic_2.3.5-9_all.ipk
├── luci-app-vlmcsd_1.0-5_all.ipk
├── luci-app-vsftpd_1.0-3_all.ipk
├── luci-app-webadmin_2-1_all.ipk
├── luci-i18n-accesscontrol-zh-cn_1-11_all.ipk
├── luci-i18n-arpbind-zh-cn_1-3_all.ipk
├── luci-i18n-autoreboot-zh-cn_1.0-8_all.ipk
├── luci-i18n-cpufreq-zh-cn_1-5_all.ipk
├── luci-i18n-filetransfer-zh-cn_1-2_all.ipk
├── luci-i18n-ramfree-zh-cn_1.0-1_all.ipk
├── luci-i18n-sfe-zh-cn_1.0-13_all.ipk
├── luci-i18n-ttyd-zh-cn_1.0-3_all.ipk
├── luci-i18n-unblockmusic-zh-cn_2.3.5-9_all.ipk
├── luci-i18n-vlmcsd-zh-cn_1.0-5_all.ipk
├── luci-i18n-vsftpd-zh-cn_1.0-3_all.ipk
├── luci-i18n-webadmin-zh-cn_2-1_all.ipk
├── luci-lib-fs_1.0-1_all.ipk
├── microsocks_1.0-1_arm_cortex-a9.ipk
├── netifd_2020-06-06-51e9fb81-1_arm_cortex-a9.ipk
├── openssl-util_1.1.1g-1_arm_cortex-a9.ipk
├── openwrt-keyring_2019-07-25-8080ef34-1_arm_cortex-a9.ipk
├── opkg_2020-05-07-f2166a89-1_arm_cortex-a9.ipk
├── Packages
├── Packages.gz
├── Packages.manifest
├── Packages.sig
├── pdnsd-alt_1.2.9b-par-a8e46ccba7b0fa2230d6c42ab6dcd92926f6c21d_arm_cortex-a9.ipk
├── ppp_2.4.8-5_arm_cortex-a9.ipk
├── ppp-mod-pppoe_2.4.8-5_arm_cortex-a9.ipk
├── procd_2020-05-28-b9b39e20-2_arm_cortex-a9.ipk
├── redsocks2_0.67-4_arm_cortex-a9.ipk
├── resolveip_2_arm_cortex-a9.ipk
├── rpcd_2020-05-26-078bb57e-1_arm_cortex-a9.ipk
├── shadowsocksr-libev-alt_2.5.6-5_arm_cortex-a9.ipk
├── shadowsocksr-libev-server_2.5.6-5_arm_cortex-a9.ipk
├── shadowsocksr-libev-ssr-local_2.5.6-5_arm_cortex-a9.ipk
├── shellsync_0.2-2_arm_cortex-a9.ipk
├── simple-obfs_0.0.5-5_arm_cortex-a9.ipk
├── swconfig_12_arm_cortex-a9.ipk
├── trojan_1.16.0-1_arm_cortex-a9.ipk
├── ubox_2019-12-31-0e34af14-4_arm_cortex-a9.ipk
├── ubus_2020-02-05-171469e3-1_arm_cortex-a9.ipk
├── ubusd_2020-02-05-171469e3-1_arm_cortex-a9.ipk
├── uci_2018-08-11-4c8b4d6e-2_arm_cortex-a9.ipk
├── uclient-fetch_2020-06-17-c6609861-1_arm_cortex-a9.ipk
├── uhttpd_2020-06-03-939c281c-2_arm_cortex-a9.ipk
├── uhttpd-mod-ubus_2020-06-03-939c281c-2_arm_cortex-a9.ipk
├── UnblockNeteaseMusicGo_0.2.4-1_arm_cortex-a9.ipk
├── urandom-seed_1.0-2_arm_cortex-a9.ipk
├── urngd_2020-01-21-c7f7b6b6-1_arm_cortex-a9.ipk
├── usign_2020-05-23-f1f65026-1_arm_cortex-a9.ipk
├── v2ray_4.27.4-1_arm_cortex-a9.ipk
├── v2ray-plugin_1.4.1-1_arm_cortex-a9.ipk
├── vlmcsd_svn1113-1_arm_cortex-a9.ipk
├── vsftpd-alt_3.0.3-7_arm_cortex-a9.ipk
├── wget_1.20.3-4_arm_cortex-a9.ipk
├── wireless-regdb_2020.04.29-1_all.ipk
├── wol_0.7.1-3_arm_cortex-a9.ipk
├── wpad-basic_2020-06-08-5a8b3662-4_arm_cortex-a9.ipk
└── zlib_1.2.11-3_arm_cortex-a9.ipk

0 directories, 113 files
```

插件
[GitHub](https://mrxn.net/tag/github)
仓库链接：
  
  
<https://github.com/Mr-xn/k3_packages_backup>
  
  
参考链接：
  
  

<https://netflixcn.com/miji/id-50.html&nbsp>
;
  
  

<https://github.com/nondanee/UnblockNeteaseMusic/>
  
  

<https://github.com/nondanee/UnblockNeteaseMusic/issues/48#issuecomment-477870013>

* 标签：
* [#
  分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#
  github](https://mrxn.net/tag/github)

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
[OpenWrt UnblockNeteaseMusicGo 插件 证书过期替换](https://mrxn.net/jswz/674.html)
  
文章链接：
<https://mrxn.net/jswz/674.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/674.html"),
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
text: encodeURI("https://mrxn.net/jswz/674.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});